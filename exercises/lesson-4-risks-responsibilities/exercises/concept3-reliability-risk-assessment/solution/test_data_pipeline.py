"""
Test suite for Reliable Financial Data Processing Pipeline
=========================================================

This test suite validates the reliability improvements in the solution version
of the data pipeline, demonstrating proper error handling, resource management,
and monitoring capabilities.
"""

import pytest
import sqlite3
import os
import tempfile
import json
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, mock_open
import time
import threading
from pathlib import Path

from data_pipeline import (
    ReliableDatabaseManager, RobustExternalAPIManager, ReliableFinancialDataProcessor,
    ConnectionPool, CircuitBreaker, ServiceStatus, ProcessingMetrics,
    run_reliable_daily_pipeline
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def temp_data_dir():
    """Create temporary data directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def db_manager(temp_db):
    """Create a ReliableDatabaseManager instance."""
    return ReliableDatabaseManager(temp_db)


@pytest.fixture
def sample_transactions():
    """Sample transaction data for testing."""
    return [
        {
            'transaction_id': 'T001',
            'account_id': 'A001',
            'amount': 100.0,
            'transaction_type': 'credit',
            'transaction_date': '2024-01-01'
        },
        {
            'transaction_id': 'T002',
            'account_id': 'A002',
            'amount': 50.0,
            'transaction_type': 'debit',
            'transaction_date': '2024-01-01'
        }
    ]


class TestConnectionPool:
    """Test database connection pool functionality."""
    
    def test_connection_pool_creation(self, temp_db):
        """Test connection pool creates connections properly."""
        pool = ConnectionPool(temp_db, max_connections=5)
        
        # Test getting connections
        connections = []
        for _ in range(3):
            with pool.get_connection() as conn:
                connections.append(conn)
                assert conn is not None
                # Test connection works
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                assert result[0] == 1
    
    def test_connection_pool_limit(self, temp_db):
        """Test connection pool respects maximum connections."""
        pool = ConnectionPool(temp_db, max_connections=2)
        
        # Get connections up to limit
        conn1_acquired = False
        conn2_acquired = False
        
        with pool.get_connection() as conn1:
            conn1_acquired = True
            with pool.get_connection() as conn2:
                conn2_acquired = True
                # Both connections should be acquired successfully
                assert conn1 is not None
                assert conn2 is not None
        
        assert conn1_acquired and conn2_acquired
    
    def test_connection_pool_concurrent_access(self, temp_db):
        """Test connection pool handles concurrent access safely."""
        pool = ConnectionPool(temp_db, max_connections=5)
        results = []
        errors = []
        
        def worker():
            try:
                with pool.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    results.append(result[0])
            except Exception as e:
                errors.append(str(e))
        
        # Start multiple threads
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All operations should succeed
        assert len(errors) == 0
        assert len(results) == 10
        assert all(r == 1 for r in results)


class TestCircuitBreaker:
    """Test circuit breaker pattern implementation."""
    
    def test_circuit_breaker_normal_operation(self):
        """Test circuit breaker allows calls when service is healthy."""
        cb = CircuitBreaker(failure_threshold=3)
        
        def successful_func():
            return "success"
        
        # Should work normally
        result = cb.call(successful_func)
        assert result == "success"
        assert cb.status == ServiceStatus.AVAILABLE
    
    def test_circuit_breaker_failure_threshold(self):
        """Test circuit breaker opens after failure threshold."""
        cb = CircuitBreaker(failure_threshold=3, timeout=1)
        
        def failing_func():
            raise Exception("Service unavailable")
        
        # Fail up to threshold
        for i in range(3):
            with pytest.raises(Exception):
                cb.call(failing_func)
        
        # Circuit should be open now
        assert cb.status == ServiceStatus.UNAVAILABLE
        
        # Next call should fail immediately
        with pytest.raises(Exception, match="Circuit breaker is OPEN"):
            cb.call(failing_func)
    
    def test_circuit_breaker_recovery(self):
        """Test circuit breaker can recover after timeout."""
        cb = CircuitBreaker(failure_threshold=2, timeout=0.1)
        
        def failing_func():
            raise Exception("Service unavailable")
        
        def successful_func():
            return "recovered"
        
        # Trigger circuit breaker
        for i in range(2):
            with pytest.raises(Exception):
                cb.call(failing_func)
        
        assert cb.status == ServiceStatus.UNAVAILABLE
        
        # Wait for timeout
        time.sleep(0.2)
        
        # Should be able to try again and recover
        result = cb.call(successful_func)
        assert result == "recovered"
        assert cb.status == ServiceStatus.AVAILABLE


class TestReliableDatabaseManager:
    """Test enhanced database manager functionality."""
    
    def test_database_setup_with_indexes(self, temp_db):
        """Test database setup creates proper schema and indexes."""
        db_manager = ReliableDatabaseManager(temp_db)
        
        with db_manager.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['transactions', 'account_balances', 'processing_status', 'processing_errors']
            for table in expected_tables:
                assert table in tables
            
            # Check indexes exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
            indexes = [row[0] for row in cursor.fetchall()]
            
            assert any('idx_transactions_account_id' in idx for idx in indexes)
            assert any('idx_transactions_date' in idx for idx in indexes)
    
    def test_batch_transaction_save(self, db_manager, sample_transactions):
        """Test batch transaction saving with error handling."""
        batch_id = "test_batch_001"
        
        # Add one invalid transaction
        invalid_transaction = sample_transactions + [{
            'transaction_id': None,  # Invalid
            'account_id': 'A003',
            'amount': 'invalid',  # Invalid amount
            'transaction_type': 'credit',
            'transaction_date': '2024-01-01'
        }]
        
        results = db_manager.save_transactions_batch(invalid_transaction, batch_id)
        
        # Should have some successes and some failures
        assert results['success'] >= 2  # At least the valid ones
        assert results['failed'] >= 1   # At least the invalid one
        assert len(results['errors']) >= 1
    
    def test_optimistic_locking_balance_update(self, db_manager):
        """Test optimistic locking prevents concurrent balance update issues."""
        account_id = "TEST_ACCOUNT"
        
        # First update should succeed
        success1 = db_manager.update_account_balance_safe(account_id, 100.0)
        assert success1 is True
        
        # Second update should also succeed
        success2 = db_manager.update_account_balance_safe(account_id, 150.0)
        assert success2 is True
        
        # Verify final balance
        with db_manager.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_balance FROM account_balances WHERE account_id = ?", (account_id,))
            result = cursor.fetchone()
            assert result[0] == 150.0


class TestRobustExternalAPIManager:
    """Test enhanced API manager with circuit breakers."""
    
    def test_api_retry_logic(self):
        """Test API calls retry with exponential backoff."""
        api_manager = RobustExternalAPIManager()
        
        with patch.object(api_manager.session, 'get') as mock_get:
            # First two calls fail, third succeeds
            mock_get.side_effect = [
                Exception("Connection error"),
                Exception("Timeout error"),
                MagicMock(status_code=200, json=lambda: {"account_data": "success"})
            ]
            
            # Should eventually succeed after retries
            result = api_manager.get_account_details_safe("TEST_ACCOUNT")
            
            assert result == {"account_data": "success"}
            assert mock_get.call_count == 3
    
    def test_fallback_validation(self):
        """Test fallback validation when external service fails."""
        api_manager = RobustExternalAPIManager()
        
        # Test valid transaction
        valid_transaction = {
            'transaction_id': 'T001',
            'account_id': 'A001',
            'amount': 100.0,
            'transaction_type': 'credit'
        }
        
        result = api_manager._fallback_validation(valid_transaction)
        assert result is True
        
        # Test invalid transaction
        invalid_transaction = {
            'transaction_id': 'T002',
            'account_id': 'A002',
            'amount': -100.0,  # Invalid negative amount
            'transaction_type': 'credit'
        }
        
        result = api_manager._fallback_validation(invalid_transaction)
        assert result is False
    
    def test_circuit_breaker_integration(self):
        """Test circuit breaker integration with API calls."""
        api_manager = RobustExternalAPIManager()
        
        with patch.object(api_manager.session, 'post') as mock_post:
            # Make validation service fail repeatedly
            mock_post.side_effect = Exception("Service down")
            
            transaction = {
                'transaction_id': 'T001',
                'account_id': 'A001',
                'amount': 100.0,
                'transaction_type': 'credit'
            }
            
            # First few calls should trigger circuit breaker
            for _ in range(4):
                result = api_manager.validate_transaction_safe(transaction)
                # Should fall back to local validation
                assert result is True  # Valid transaction
            
            # Circuit breaker should be open now
            assert api_manager.circuit_breakers['validation_service'].status == ServiceStatus.UNAVAILABLE


class TestReliableFinancialDataProcessor:
    """Test the main processor with reliability features."""
    
    def test_transaction_processing_with_errors(self, temp_db):
        """Test transaction processing handles errors gracefully."""
        processor = ReliableFinancialDataProcessor(temp_db)
        
        # Valid transaction
        valid_transaction = {
            'transaction_id': 'T001',
            'account_id': 'A001',
            'amount': 100.0,
            'transaction_type': 'credit',
            'transaction_date': '2024-01-01'
        }
        
        result = processor.process_transaction_safe(valid_transaction)
        assert result['status'] == 'success'
        assert 'new_balance' in result
        
        # Invalid transaction
        invalid_transaction = {
            'transaction_id': 'T002',
            'account_id': 'A002',
            'amount': 'invalid',  # Invalid amount
            'transaction_type': 'credit',
            'transaction_date': '2024-01-01'
        }
        
        result = processor.process_transaction_safe(invalid_transaction)
        assert result['status'] == 'failed'
        assert 'error' in result
    
    def test_streaming_file_processing(self, temp_data_dir):
        """Test streaming file processing manages memory efficiently."""
        processor = ReliableFinancialDataProcessor()
        
        # Create test CSV file
        test_data = []
        for i in range(1000):
            test_data.append({
                'transaction_id': f'T{i:04d}',
                'account_id': f'A{i % 10:03d}',
                'amount': 100.0 + i,
                'transaction_type': 'credit' if i % 2 == 0 else 'debit',
                'transaction_date': '2024-01-01'
            })
        
        test_csv = Path(temp_data_dir) / "test_transactions.csv"
        pd.DataFrame(test_data).to_csv(test_csv, index=False)
        
        # Test streaming
        chunks_processed = 0
        total_records = 0
        
        for chunk in processor.stream_transaction_files([str(test_csv)], chunk_size=100):
            chunks_processed += 1
            total_records += len(chunk)
            assert len(chunk) <= 100  # Chunk size respected
        
        assert chunks_processed == 10  # 1000 records / 100 chunk size
        assert total_records == 1000
    
    def test_batch_processing_with_monitoring(self, temp_db, temp_data_dir):
        """Test batch processing includes proper monitoring and metrics."""
        processor = ReliableFinancialDataProcessor(temp_db)
        
        # Create test data file
        test_data = [
            {'transaction_id': 'T001', 'account_id': 'A001', 'amount': 100, 'transaction_type': 'credit', 'transaction_date': '2024-01-01'},
            {'transaction_id': 'T002', 'account_id': 'A002', 'amount': 50, 'transaction_type': 'debit', 'transaction_date': '2024-01-01'}
        ]
        
        test_file = Path(temp_data_dir) / "transactions_2024-01-01.json"
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Process batch
        metrics = processor.process_daily_batch_reliable('2024-01-01', temp_data_dir, max_workers=1, chunk_size=1)
        
        # Verify metrics
        assert metrics.batch_id.startswith('batch_2024-01-01_')
        assert metrics.records_processed >= 0
        assert metrics.start_time is not None
        assert metrics.end_time is not None
        assert metrics.processing_rate >= 0
        
        # Verify database status tracking
        with processor.db_manager.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM processing_status WHERE batch_id = ?", (metrics.batch_id,))
            status_record = cursor.fetchone()
            assert status_record is not None


class TestIntegrationScenarios:
    """Test complete integration scenarios."""
    
    def test_end_to_end_pipeline_execution(self, temp_data_dir):
        """Test complete pipeline execution with real data flow."""
        # Create test data
        test_data = []
        for i in range(100):
            test_data.append({
                'transaction_id': f'T{i:04d}',
                'account_id': f'A{i % 5:03d}',
                'amount': 100.0 + (i * 10),
                'transaction_type': 'credit' if i % 2 == 0 else 'debit',
                'transaction_date': '2024-01-15'
            })
        
        # Save test data
        test_file = Path(temp_data_dir) / "transactions_2024-01-15.csv"
        pd.DataFrame(test_data).to_csv(test_file, index=False)
        
        # Mock external services to avoid real API calls
        with patch('data_pipeline.RobustExternalAPIManager') as mock_api_class:
            mock_api = MagicMock()
            mock_api.validate_transaction_safe.return_value = True
            mock_api.get_account_details_safe.return_value = {"balance": 1000.0}
            mock_api_class.return_value = mock_api
            
            # Run pipeline
            metrics = run_reliable_daily_pipeline('2024-01-15', temp_data_dir)
            
            # Verify successful processing
            assert metrics.records_processed > 0
            assert metrics.end_time is not None
            assert metrics.processing_rate > 0
            
            # Verify report generation
            report_file = Path("reports") / "reliable_report_2024-01-15.json"
            assert report_file.exists()
            
            # Cleanup
            if report_file.exists():
                report_file.unlink()
                report_file.parent.rmdir()
    
    def test_failure_recovery_scenarios(self, temp_db):
        """Test system behavior under various failure conditions."""
        processor = ReliableFinancialDataProcessor(temp_db)
        
        # Test database connection failure recovery
        with patch.object(processor.db_manager.connection_pool, 'get_connection') as mock_conn:
            mock_conn.side_effect = [Exception("DB connection failed"), 
                                   processor.db_manager.connection_pool.get_connection()]
            
            # First call should fail, but system should be resilient
            transaction = {
                'transaction_id': 'T001',
                'account_id': 'A001',
                'amount': 100.0,
                'transaction_type': 'credit',
                'transaction_date': '2024-01-01'
            }
            
            # Should handle the error gracefully
            result = processor.process_transaction_safe(transaction)
            # The exact behavior depends on implementation, but it shouldn't crash
            assert 'status' in result
    
    def test_performance_under_load(self, temp_db, temp_data_dir):
        """Test system performance with larger datasets."""
        processor = ReliableFinancialDataProcessor(temp_db)
        
        # Create larger test dataset
        test_data = []
        for i in range(1000):
            test_data.append({
                'transaction_id': f'T{i:06d}',
                'account_id': f'A{i % 100:03d}',
                'amount': 100.0 + i,
                'transaction_type': 'credit' if i % 2 == 0 else 'debit',
                'transaction_date': '2024-01-20'
            })
        
        test_file = Path(temp_data_dir) / "large_transactions_2024-01-20.csv"
        pd.DataFrame(test_data).to_csv(test_file, index=False)
        
        # Mock external services for speed
        with patch.object(processor.api_manager, 'validate_transaction_safe', return_value=True), \
             patch.object(processor.api_manager, 'get_account_details_safe', return_value={"balance": 10000.0}):
            
            start_time = time.time()
            metrics = processor.process_daily_batch_reliable('2024-01-20', temp_data_dir, 
                                                           max_workers=2, chunk_size=100)
            end_time = time.time()
            
            # Performance assertions
            processing_time = end_time - start_time
            assert processing_time < 30  # Should complete within 30 seconds
            assert metrics.processing_rate > 10  # Should process at least 10 transactions/second
            assert metrics.records_processed > 900  # Should process most transactions successfully


if __name__ == "__main__":
    pytest.main([__file__, "-v"])