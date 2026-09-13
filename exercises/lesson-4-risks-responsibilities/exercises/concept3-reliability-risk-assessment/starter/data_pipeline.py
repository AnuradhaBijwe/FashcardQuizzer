"""
AI-Generated Financial Data Processing Pipeline
==============================================

This module provides data processing and API integration functionality.
Generated to handle financial transaction processing efficiently.
"""

import requests
import time
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional


class ExternalAPIClient:
    """Handles external API calls for data enrichment."""
    
    def __init__(self, base_url: str = "https://api.financial-service.com"):
        self.base_url = base_url
        self.timeout = 30
    
    def get_exchange_rate(self, currency: str) -> Dict[str, Any]:
        """Get current exchange rate for currency."""
        # No retry logic or circuit breaker
        url = f"{self.base_url}/rates/{currency}"
        response = requests.get(url, timeout=self.timeout)
        
        # Direct response processing without error handling
        return response.json()
    
    def validate_account(self, account_id: str) -> bool:
        """Validate account ID with external service."""
        url = f"{self.base_url}/accounts/{account_id}/validate"
        
        # No error handling for network failures
        response = requests.get(url, timeout=self.timeout)
        
        if response.status_code == 200:
            return response.json()["valid"]
        else:
            # Fails without fallback
            raise Exception(f"Account validation failed: {response.status_code}")


class TransactionProcessor:
    """Processes financial transactions."""
    
    def __init__(self, database_path: str = "transactions.db"):
        self.database_path = database_path
        self.api_client = ExternalAPIClient()
        self.setup_database()
    
    def setup_database(self):
        """Initialize database."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def process_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single transaction with external validation."""
        account_id = transaction["account_id"]
        amount = transaction["amount"]
        currency = transaction["currency"]
        
        # Step 1: Validate account (can fail without retry)
        is_valid = self.api_client.validate_account(account_id)
        if not is_valid:
            return {"status": "failed", "reason": "Invalid account"}
        
        # Step 2: Get exchange rate (can fail without fallback)
        if currency != "USD":
            rate_data = self.api_client.get_exchange_rate(currency)
            usd_amount = amount * rate_data["rate"]
        else:
            usd_amount = amount
        
        # Step 3: Save to database (can fail without rollback)
        self._save_transaction(account_id, usd_amount, "USD", "completed")
        
        return {
            "status": "completed",
            "account_id": account_id,
            "original_amount": amount,
            "usd_amount": usd_amount,
            "currency": currency
        }
    
    def process_batch(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process multiple transactions."""
        results = {
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        for transaction in transactions:
            try:
                # No partial failure handling
                result = self.process_transaction(transaction)
                if result["status"] == "completed":
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(result["reason"])
            
            except Exception as e:
                # Continues processing even after failures
                results["failed"] += 1
                results["errors"].append(str(e))
                # No circuit breaker to stop cascade failures
                continue
        
        return results
    
    def _save_transaction(self, account_id: str, amount: float, 
                         currency: str, status: str):
        """Save transaction to database."""
        # No connection pooling or transaction management
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions (account_id, amount, currency, status)
            VALUES (?, ?, ?, ?)
        """, (account_id, amount, currency, status))
        
        # No error handling for database failures
        conn.commit()
        conn.close()
    
    def get_transaction_summary(self) -> Dict[str, Any]:
        """Get summary of all transactions."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # No error handling for query failures
        cursor.execute("""
            SELECT status, COUNT(*), SUM(amount)
            FROM transactions
            GROUP BY status
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        summary = {}
        for status, count, total in results:
            summary[status] = {"count": count, "total_amount": total}
        
        return summary


class DataPipelineOrchestrator:
    """Orchestrates the entire data processing pipeline."""
    
    def __init__(self):
        self.processor = TransactionProcessor()
        self.last_run = None
    
    def run_daily_pipeline(self, data_source: str) -> Dict[str, Any]:
        """Run the daily data processing pipeline."""
        start_time = time.time()
        
        # Step 1: Get data (no validation)
        raw_data = self._fetch_data_from_source(data_source)
        
        # Step 2: Process all data (no error recovery)
        batch_result = self.processor.process_batch(raw_data)
        
        # Step 3: Generate summary (no failure handling)
        summary = self.processor.get_transaction_summary()
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.last_run = datetime.now()
        
        return {
            "pipeline_status": "completed",
            "duration_seconds": duration,
            "batch_result": batch_result,
            "summary": summary,
            "processed_at": self.last_run.isoformat()
        }
    
    def _fetch_data_from_source(self, source: str) -> List[Dict[str, Any]]:
        """Fetch data from external source."""
        # Simulated data - no actual external dependency
        if source == "demo":
            return [
                {"account_id": "ACC001", "amount": 100.50, "currency": "USD"},
                {"account_id": "ACC002", "amount": 75.25, "currency": "EUR"},
                {"account_id": "ACC003", "amount": 200.00, "currency": "GBP"},
                {"account_id": "INVALID", "amount": 50.00, "currency": "USD"},  # Will fail validation
                {"account_id": "ACC004", "amount": 150.75, "currency": "JPY"}
            ]
        else:
            # No fallback for unknown sources
            raise ValueError(f"Unknown data source: {source}")


def create_sample_pipeline():
    """Create a sample pipeline for testing."""
    return DataPipelineOrchestrator()


if __name__ == "__main__":
    # Demo the pipeline
    pipeline = create_sample_pipeline()
    
    print("=== Financial Data Pipeline Demo ===")
    
    try:
        result = pipeline.run_daily_pipeline("demo")
        print(f"Pipeline completed in {result['duration_seconds']:.2f} seconds")
        print(f"Successful transactions: {result['batch_result']['successful']}")
        print(f"Failed transactions: {result['batch_result']['failed']}")
        if result['batch_result']['errors']:
            print(f"Errors: {result['batch_result']['errors']}")
    
    except Exception as e:
        print(f"Pipeline failed completely: {e}")
        
    print("\n=== Reliability Issues ===")
    print("⚠️  No retry logic for failed API calls")
    print("⚠️  No circuit breaker for cascade failures")
    print("⚠️  No fallback mechanisms for external dependencies")
    print("⚠️  No transaction rollback on partial failures")
    print("⚠️  No connection pooling or resource management")