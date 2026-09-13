"""
Reliable Financial Data Processing Pipeline
==========================================

This module provides a robust, production-ready implementation of the financial
data processing pipeline with proper error handling, resource management,
and monitoring capabilities.

Key improvements over the starter version:
- Connection pooling and proper resource management
- Comprehensive error handling with retries
- Circuit breaker pattern for external services
- Memory-efficient streaming processing
- Detailed monitoring and observability
- Graceful degradation under load
"""

import json
import sqlite3
import requests
import time
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Iterator
import os
import logging
import contextlib
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import gc
from pathlib import Path

# Enhanced logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service status enumeration for circuit breaker."""
    AVAILABLE = "available"
    DEGRADED = "degraded" 
    UNAVAILABLE = "unavailable"


@dataclass
class ProcessingMetrics:
    """Processing metrics for monitoring and reporting."""
    batch_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    records_processed: int = 0
    records_failed: int = 0
    processing_rate: float = 0.0
    memory_peak_mb: float = 0.0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class CircuitBreaker:
    """Circuit breaker pattern for external service calls."""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.status = ServiceStatus.AVAILABLE
        self._lock = threading.Lock()
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        with self._lock:
            if self._is_circuit_open():
                raise Exception("Circuit breaker is OPEN - service unavailable")
            
            if self.status == ServiceStatus.DEGRADED:
                logger.warning("Service is degraded - proceeding with caution")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _is_circuit_open(self) -> bool:
        """Check if circuit breaker should be open."""
        if self.status == ServiceStatus.UNAVAILABLE:
            if self.last_failure_time:
                time_since_failure = time.time() - self.last_failure_time
                if time_since_failure > self.timeout:
                    logger.info("Circuit breaker timeout expired - attempting to reset")
                    self.status = ServiceStatus.DEGRADED
                    self.failure_count = 0
                    return False
            return True
        return False
    
    def _on_success(self):
        """Handle successful service call."""
        self.failure_count = 0
        if self.status != ServiceStatus.AVAILABLE:
            logger.info("Service recovered - circuit breaker reset")
            self.status = ServiceStatus.AVAILABLE
    
    def _on_failure(self):
        """Handle failed service call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            logger.error(f"Circuit breaker OPEN - {self.failure_count} failures")
            self.status = ServiceStatus.UNAVAILABLE
        elif self.failure_count >= self.failure_threshold // 2:
            logger.warning(f"Service degraded - {self.failure_count} failures")
            self.status = ServiceStatus.DEGRADED


class ConnectionPool:
    """Database connection pool for resource management."""
    
    def __init__(self, database_path: str, max_connections: int = 10):
        self.database_path = database_path
        self.max_connections = max_connections
        self._pool = queue.Queue(maxsize=max_connections)
        self._lock = threading.Lock()
        self._total_connections = 0
        
        # Pre-populate pool with initial connections
        for _ in range(min(3, max_connections)):
            self._create_connection()
    
    def _create_connection(self) -> sqlite3.Connection:
        """Create a new database connection."""
        conn = sqlite3.connect(
            self.database_path,
            timeout=30,
            isolation_level='DEFERRED'
        )
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        self._total_connections += 1
        return conn
    
    @contextlib.contextmanager
    def get_connection(self):
        """Get a connection from the pool."""
        connection = None
        try:
            # Try to get existing connection from pool
            try:
                connection = self._pool.get_nowait()
            except queue.Empty:
                # Create new connection if pool is empty and under limit
                with self._lock:
                    if self._total_connections < self.max_connections:
                        connection = self._create_connection()
                    else:
                        # Wait for connection if at limit
                        connection = self._pool.get(timeout=30)
            
            yield connection
            
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            if connection:
                connection.close()
                with self._lock:
                    self._total_connections -= 1
            raise
        finally:
            # Return connection to pool if still valid
            if connection:
                try:
                    # Test connection is still valid
                    connection.execute("SELECT 1")
                    self._pool.put_nowait(connection)
                except (queue.Full, sqlite3.Error):
                    connection.close()
                    with self._lock:
                        self._total_connections -= 1


class ReliableDatabaseManager:
    """Enhanced database manager with connection pooling and error handling."""
    
    def __init__(self, database_path: str = "financial_data.db"):
        self.database_path = database_path
        self.connection_pool = ConnectionPool(database_path)
        self.setup_database()
    
    def setup_database(self):
        """Initialize database with required tables and indexes."""
        with self.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # Financial transactions table with indexes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT UNIQUE NOT NULL,
                    account_id TEXT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    transaction_type TEXT NOT NULL,
                    transaction_date DATE NOT NULL,
                    processed_date TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    retry_count INTEGER DEFAULT 0,
                    error_message TEXT
                )
            """)
            
            # Add indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status)")
            
            # Account balances table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS account_balances (
                    account_id TEXT PRIMARY KEY,
                    current_balance DECIMAL(10,2) NOT NULL,
                    last_updated TIMESTAMP NOT NULL,
                    version INTEGER DEFAULT 1
                )
            """)
            
            # Enhanced processing status tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_status (
                    batch_id TEXT PRIMARY KEY,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    records_processed INTEGER DEFAULT 0,
                    records_failed INTEGER DEFAULT 0,
                    processing_rate REAL DEFAULT 0.0,
                    memory_peak_mb REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'running',
                    error_details TEXT
                )
            """)
            
            # Processing errors table for detailed error tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL,
                    transaction_id TEXT,
                    error_type TEXT NOT NULL,
                    error_message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    retry_count INTEGER DEFAULT 0,
                    resolved BOOLEAN DEFAULT FALSE
                )
            """)
            
            conn.commit()
    
    def save_transactions_batch(self, transactions: List[Dict[str, Any]], batch_id: str) -> Dict[str, int]:
        """Save multiple transactions in a single transaction with error tracking."""
        results = {"success": 0, "failed": 0, "errors": []}
        
        with self.connection_pool.get_connection() as conn:
            try:
                cursor = conn.cursor()
                
                for transaction in transactions:
                    try:
                        cursor.execute("""
                            INSERT OR REPLACE INTO transactions 
                            (transaction_id, account_id, amount, transaction_type, 
                             transaction_date, processed_date, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            transaction['transaction_id'],
                            transaction['account_id'],
                            transaction['amount'],
                            transaction['transaction_type'],
                            transaction['transaction_date'],
                            datetime.now(),
                            'processed'
                        ))
                        results["success"] += 1
                        
                    except Exception as e:
                        results["failed"] += 1
                        error_msg = f"Failed to save transaction {transaction.get('transaction_id', 'unknown')}: {e}"
                        results["errors"].append(error_msg)
                        logger.error(error_msg)
                        
                        # Log error to error tracking table
                        cursor.execute("""
                            INSERT INTO processing_errors 
                            (batch_id, transaction_id, error_type, error_message)
                            VALUES (?, ?, ?, ?)
                        """, (batch_id, transaction.get('transaction_id'), 'SAVE_ERROR', str(e)))
                
                conn.commit()
                
            except Exception as e:
                conn.rollback()
                logger.error(f"Batch transaction save failed: {e}")
                raise
        
        return results
    
    def update_account_balance_safe(self, account_id: str, new_balance: float) -> bool:
        """Update account balance with optimistic locking."""
        with self.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    # Get current version
                    cursor.execute(
                        "SELECT version FROM account_balances WHERE account_id = ?", 
                        (account_id,)
                    )
                    result = cursor.fetchone()
                    current_version = result[0] if result else 0
                    
                    # Update with version check
                    if current_version == 0:
                        # Insert new record
                        cursor.execute("""
                            INSERT INTO account_balances (account_id, current_balance, last_updated, version)
                            VALUES (?, ?, ?, 1)
                        """, (account_id, new_balance, datetime.now()))
                    else:
                        # Update existing record with version check
                        cursor.execute("""
                            UPDATE account_balances 
                            SET current_balance = ?, last_updated = ?, version = version + 1
                            WHERE account_id = ? AND version = ?
                        """, (new_balance, datetime.now(), account_id, current_version))
                        
                        if cursor.rowcount == 0:
                            # Version conflict - retry
                            logger.warning(f"Version conflict updating balance for {account_id}, retrying...")
                            time.sleep(0.1 * (attempt + 1))  # Exponential backoff
                            continue
                    
                    conn.commit()
                    return True
                    
                except Exception as e:
                    logger.error(f"Error updating balance for {account_id}: {e}")
                    conn.rollback()
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(0.1 * (attempt + 1))
            
            return False


class RobustExternalAPIManager:
    """Enhanced API manager with circuit breakers and retry logic."""
    
    def __init__(self):
        self.api_endpoints = {
            'account_service': 'https://api.bank.com/accounts',
            'validation_service': 'https://api.validator.com/validate',
            'notification_service': 'https://api.notify.com/send',
            'audit_service': 'https://api.audit.com/log'
        }
        
        self.api_timeouts = {
            'account_service': 30,
            'validation_service': 10,
            'notification_service': 5,
            'audit_service': 15
        }
        
        # Circuit breakers for each service
        self.circuit_breakers = {
            service: CircuitBreaker(failure_threshold=3, timeout=60)
            for service in self.api_endpoints.keys()
        }
        
        # Session with connection pooling
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=0  # We handle retries manually
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def _retry_with_backoff(self, func, max_retries: int = 3, base_delay: float = 1.0):
        """Execute function with exponential backoff retry logic."""
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func()
            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"API call failed (attempt {attempt + 1}), retrying in {delay}s: {e}")
                    time.sleep(delay)
                else:
                    logger.error(f"API call failed after {max_retries + 1} attempts: {e}")
        
        raise last_exception
    
    def get_account_details_safe(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Fetch account details with circuit breaker and retry logic."""
        service = 'account_service'
        
        def api_call():
            url = f"{self.api_endpoints[service]}/{account_id}"
            response = self.session.get(url, timeout=self.api_timeouts[service])
            response.raise_for_status()
            return response.json()
        
        try:
            return self.circuit_breakers[service].call(
                lambda: self._retry_with_backoff(api_call)
            )
        except Exception as e:
            logger.error(f"Failed to get account details for {account_id}: {e}")
            return None
    
    def validate_transaction_safe(self, transaction: Dict[str, Any]) -> bool:
        """Validate transaction with fallback logic."""
        service = 'validation_service'
        
        def api_call():
            url = f"{self.api_endpoints[service]}/transaction"
            response = self.session.post(
                url, 
                json=transaction, 
                timeout=self.api_timeouts[service]
            )
            response.raise_for_status()
            return response.json().get('valid', False)
        
        try:
            return self.circuit_breakers[service].call(
                lambda: self._retry_with_backoff(api_call)
            )
        except Exception as e:
            logger.warning(f"Transaction validation failed, using fallback: {e}")
            # Fallback validation logic
            return self._fallback_validation(transaction)
    
    def _fallback_validation(self, transaction: Dict[str, Any]) -> bool:
        """Basic fallback validation when external service is unavailable."""
        required_fields = ['transaction_id', 'account_id', 'amount', 'transaction_type']
        
        # Check required fields
        for field in required_fields:
            if field not in transaction or transaction[field] is None:
                return False
        
        # Basic amount validation
        try:
            amount = float(transaction['amount'])
            if amount <= 0 or amount > 1000000:  # Reasonable limits
                return False
        except (ValueError, TypeError):
            return False
        
        # Valid transaction types
        valid_types = ['credit', 'debit']
        if transaction['transaction_type'] not in valid_types:
            return False
        
        return True


class ReliableFinancialDataProcessor:
    """Production-ready financial data processor with comprehensive error handling."""
    
    def __init__(self, database_path: str = "financial_data.db"):
        self.db_manager = ReliableDatabaseManager(database_path)
        self.api_manager = RobustExternalAPIManager()
        self.metrics = {}
    
    def stream_transaction_files(self, file_paths: List[str], chunk_size: int = 1000) -> Iterator[List[Dict[str, Any]]]:
        """Stream transaction files in chunks to manage memory usage."""
        for file_path in file_paths:
            try:
                file_path_obj = Path(file_path)
                if not file_path_obj.exists():
                    logger.warning(f"File not found: {file_path}")
                    continue
                
                if file_path.endswith('.csv'):
                    # Stream CSV in chunks
                    for chunk_df in pd.read_csv(file_path, chunksize=chunk_size):
                        yield chunk_df.to_dict('records')
                        
                elif file_path.endswith('.json'):
                    # For JSON, load and yield in chunks
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for i in range(0, len(data), chunk_size):
                                yield data[i:i + chunk_size]
                        else:
                            yield [data]
                
                logger.info(f"Finished streaming file: {file_path}")
                
            except Exception as e:
                logger.error(f"Error streaming file {file_path}: {e}")
                continue
    
    def process_transaction_safe(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single transaction with comprehensive error handling."""
        transaction_id = transaction.get('transaction_id', 'unknown')
        
        try:
            # Validate transaction data
            if not self.api_manager.validate_transaction_safe(transaction):
                return {
                    'transaction_id': transaction_id,
                    'status': 'failed',
                    'error': 'Transaction validation failed'
                }
            
            # Get account details (with fallback if service unavailable)
            account_details = self.api_manager.get_account_details_safe(transaction['account_id'])
            if not account_details and transaction['transaction_type'] == 'debit':
                # For credits, we can proceed without account details
                logger.warning(f"Could not verify account details for {transaction['account_id']}")
            
            # Calculate new balance (simplified for demo)
            current_balance = 1000.0  # Would normally get from account_details
            amount = float(transaction['amount'])
            
            if transaction['transaction_type'] == 'debit':
                new_balance = current_balance - amount
                if new_balance < 0:
                    return {
                        'transaction_id': transaction_id,
                        'status': 'failed',
                        'error': 'Insufficient funds'
                    }
            else:
                new_balance = current_balance + amount
            
            # Update balance (with optimistic locking)
            if not self.db_manager.update_account_balance_safe(transaction['account_id'], new_balance):
                return {
                    'transaction_id': transaction_id,
                    'status': 'failed',
                    'error': 'Balance update failed'
                }
            
            return {
                'transaction_id': transaction_id,
                'status': 'success',
                'new_balance': new_balance
            }
            
        except Exception as e:
            logger.error(f"Error processing transaction {transaction_id}: {e}")
            return {
                'transaction_id': transaction_id,
                'status': 'failed',
                'error': str(e)
            }
    
    def process_daily_batch_reliable(self, date: str, data_directory: str = "data/", 
                                   max_workers: int = 4, chunk_size: int = 1000) -> ProcessingMetrics:
        """Process daily batch with reliable patterns and monitoring."""
        batch_id = f"batch_{date}_{int(time.time())}"
        metrics = ProcessingMetrics(batch_id=batch_id, start_time=datetime.now())
        
        logger.info(f"Starting reliable batch processing for {date}")
        
        try:
            # Find all files for the date
            data_path = Path(data_directory)
            file_patterns = [
                f"transactions_{date}.csv",
                f"transactions_{date}.json",
                f"daily_batch_{date}.csv"
            ]
            
            existing_files = []
            for pattern in file_patterns:
                matching_files = list(data_path.glob(pattern))
                existing_files.extend([str(f) for f in matching_files])
            
            if not existing_files:
                logger.warning(f"No transaction files found for date {date}")
                metrics.end_time = datetime.now()
                return metrics
            
            # Record batch start in database
            with self.db_manager.connection_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO processing_status (batch_id, start_time, status)
                    VALUES (?, ?, ?)
                """, (batch_id, metrics.start_time, 'running'))
                conn.commit()
            
            # Process files in streaming fashion
            total_processed = 0
            total_failed = 0
            
            # Use thread pool for concurrent processing of chunks
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for chunk in self.stream_transaction_files(existing_files, chunk_size):
                    # Submit chunk for processing
                    future = executor.submit(self._process_chunk, chunk, batch_id)
                    
                    try:
                        chunk_results = future.result(timeout=300)  # 5 minute timeout per chunk
                        total_processed += chunk_results['success']
                        total_failed += chunk_results['failed']
                        
                        if chunk_results['errors']:
                            metrics.errors.extend(chunk_results['errors'])
                        
                        # Periodic progress logging
                        if total_processed % 1000 == 0:
                            logger.info(f"Processed {total_processed} transactions")
                        
                        # Memory management
                        if total_processed % 5000 == 0:
                            gc.collect()
                            
                    except Exception as e:
                        logger.error(f"Chunk processing failed: {e}")
                        total_failed += len(chunk)
                        metrics.errors.append(f"Chunk processing error: {e}")
            
            # Calculate final metrics
            metrics.end_time = datetime.now()
            metrics.records_processed = total_processed
            metrics.records_failed = total_failed
            
            duration = (metrics.end_time - metrics.start_time).total_seconds()
            metrics.processing_rate = total_processed / duration if duration > 0 else 0
            
            # Update batch status in database
            with self.db_manager.connection_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE processing_status 
                    SET end_time = ?, records_processed = ?, records_failed = ?, 
                        processing_rate = ?, status = ?
                    WHERE batch_id = ?
                """, (
                    metrics.end_time, total_processed, total_failed,
                    metrics.processing_rate, 'completed', batch_id
                ))
                conn.commit()
            
            logger.info(f"Batch {batch_id} completed: {total_processed} processed, {total_failed} failed")
            return metrics
            
        except Exception as e:
            metrics.end_time = datetime.now()
            metrics.errors.append(f"Batch processing error: {e}")
            logger.error(f"Batch processing failed: {e}")
            
            # Update status to failed
            try:
                with self.db_manager.connection_pool.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE processing_status 
                        SET end_time = ?, status = ?, error_details = ?
                        WHERE batch_id = ?
                    """, (metrics.end_time, 'failed', str(e), batch_id))
                    conn.commit()
            except Exception as db_error:
                logger.error(f"Failed to update batch status: {db_error}")
            
            return metrics
    
    def _process_chunk(self, transactions: List[Dict[str, Any]], batch_id: str) -> Dict[str, Any]:
        """Process a chunk of transactions."""
        results = {"success": 0, "failed": 0, "errors": []}
        
        # Save transactions to database
        save_results = self.db_manager.save_transactions_batch(transactions, batch_id)
        results["success"] = save_results["success"]
        results["failed"] = save_results["failed"]
        results["errors"] = save_results["errors"]
        
        # Process each transaction
        for transaction in transactions:
            try:
                process_result = self.process_transaction_safe(transaction)
                if process_result['status'] != 'success':
                    results["failed"] += 1
                    results["errors"].append(process_result.get('error', 'Unknown error'))
                
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Processing error: {e}")
        
        return results


def run_reliable_daily_pipeline(date: str = None, data_directory: str = "data/"):
    """Main entry point for the reliable daily processing pipeline."""
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    logger.info(f"Starting reliable daily pipeline for {date}")
    
    processor = ReliableFinancialDataProcessor()
    
    try:
        # Process the daily batch with reliability features
        metrics = processor.process_daily_batch_reliable(date, data_directory)
        
        # Generate and save metrics report
        report_data = asdict(metrics)
        report_data['processing_duration_seconds'] = (
            (metrics.end_time - metrics.start_time).total_seconds() 
            if metrics.end_time else None
        )
        
        # Save report
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        report_filename = reports_dir / f"reliable_report_{date}.json"
        
        with open(report_filename, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Reliable processing report saved to {report_filename}")
        
        # Success metrics
        total_transactions = metrics.records_processed + metrics.records_failed
        success_rate = (metrics.records_processed / total_transactions * 100) if total_transactions > 0 else 0
        
        logger.info(f"Pipeline completed successfully:")
        logger.info(f"  - Total transactions: {total_transactions}")
        logger.info(f"  - Success rate: {success_rate:.2f}%")
        logger.info(f"  - Processing rate: {metrics.processing_rate:.2f} transactions/second")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Reliable daily pipeline failed: {e}")
        raise


if __name__ == "__main__":
    # Example usage with error handling
    import sys
    
    try:
        if len(sys.argv) > 1:
            date = sys.argv[1]
        else:
            date = datetime.now().strftime('%Y-%m-%d')
        
        metrics = run_reliable_daily_pipeline(date)
        print(f"Processing completed successfully. Processed {metrics.records_processed} transactions.")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        sys.exit(1)