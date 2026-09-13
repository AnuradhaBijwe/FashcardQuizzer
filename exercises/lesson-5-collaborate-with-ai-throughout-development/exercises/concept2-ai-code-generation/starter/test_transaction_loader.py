"""
Streamlined tests for TransactionLoader implementation.
Reduced from 17 to 12 essential tests with better organization and hints.

Tests are grouped by difficulty to guide progressive implementation.
"""
import pytest
from pathlib import Path
import tempfile
import os

# Students will create this module
try:
    from transaction_loader import CSVTransactionLoader
    IMPLEMENTATION_EXISTS = True
except ImportError:
    IMPLEMENTATION_EXISTS = False
    CSVTransactionLoader = None


@pytest.fixture
def temp_csv_file():
    """Create temporary CSV file for testing."""
    fd, path = tempfile.mkstemp(suffix='.csv')
    yield path
    os.close(fd)
    os.unlink(path)


@pytest.fixture
def valid_transactions_csv(temp_csv_file):
    """Create valid CSV file with transactions."""
    with open(temp_csv_file, 'w') as f:
        f.write("date,amount,category,description\n")
        f.write("2024-01-15,45.50,Food,Grocery shopping\n")
        f.write("2024-01-16,120.00,Transport,Gas\n")
        f.write("2024-01-17,25.99,Food,Restaurant\n")
    return temp_csv_file


# === PHASE 1: Basic Implementation (3 tests) ===
# Hint: Start here - get basic CSV loading working first

@pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not created yet")
class TestBasicLoading:
    """Phase 1: Get basic CSV loading working."""
    
    def test_can_create_loader(self):
        """Should be able to instantiate CSVTransactionLoader.
        
        Hint: Create a class CSVTransactionLoader with a load() method.
        """
        loader = CSVTransactionLoader()
        assert loader is not None
    
    def test_loads_valid_csv(self, valid_transactions_csv):
        """Should load valid CSV and return list of transactions.
        
        Hint: Use csv.DictReader to parse the CSV file.
        Return a list of dictionaries.
        """
        loader = CSVTransactionLoader()
        transactions = loader.load(valid_transactions_csv)
        
        assert isinstance(transactions, list)
        assert len(transactions) == 3
    
    def test_transaction_has_required_fields(self, valid_transactions_csv):
        """Each transaction should have all required fields.
        
        Hint: Required fields are: date, amount, category, description
        """
        loader = CSVTransactionLoader()
        transactions = loader.load(valid_transactions_csv)
        
        required_fields = {'date', 'amount', 'category', 'description'}
        for transaction in transactions:
            assert required_fields.issubset(transaction.keys())


# === PHASE 2: Data Validation (5 tests) ===
# Hint: Once basic loading works, add validation

@pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not created yet")
class TestDataValidation:
    """Phase 2: Validate data types and values."""
    
    def test_amount_converted_to_float(self, valid_transactions_csv):
        """Amount should be converted from string to float.
        
        Hint: Use float() to convert the amount column.
        """
        loader = CSVTransactionLoader()
        transactions = loader.load(valid_transactions_csv)
        
        for transaction in transactions:
            assert isinstance(transaction['amount'], float)
    
    def test_rejects_negative_amounts(self, temp_csv_file):
        """Should raise ValueError for negative amounts.
        
        Hint: After converting to float, check if amount < 0
        """
        with open(temp_csv_file, 'w') as f:
            f.write("date,amount,category,description\n")
            f.write("2024-01-15,-45.50,Food,Refund\n")
        
        loader = CSVTransactionLoader()
        with pytest.raises(ValueError):
            loader.load(temp_csv_file)
    
    def test_rejects_non_numeric_amounts(self, temp_csv_file):
        """Should raise ValueError for non-numeric amounts.
        
        Hint: Catch ValueError from float() conversion and re-raise with helpful message.
        """
        with open(temp_csv_file, 'w') as f:
            f.write("date,amount,category,description\n")
            f.write("2024-01-15,invalid,Food,Grocery\n")
        
        loader = CSVTransactionLoader()
        with pytest.raises(ValueError):
            loader.load(temp_csv_file)
    
    def test_rejects_empty_required_fields(self, temp_csv_file):
        """Should raise ValueError if required fields are empty.
        
        Hint: Check each required field with: if not row['field'].strip()
        """
        with open(temp_csv_file, 'w') as f:
            f.write("date,amount,category,description\n")
            f.write("2024-01-15,45.50,,Grocery\n")  # empty category
        
        loader = CSVTransactionLoader()
        with pytest.raises(ValueError):
            loader.load(temp_csv_file)
    
    def test_rejects_missing_columns(self, temp_csv_file):
        """Should raise ValueError if required columns are missing.
        
        Hint: Check that required columns exist in reader.fieldnames
        """
        with open(temp_csv_file, 'w') as f:
            f.write("date,amount,category\n")  # missing description
            f.write("2024-01-15,45.50,Food\n")
        
        loader = CSVTransactionLoader()
        with pytest.raises(ValueError):
            loader.load(temp_csv_file)


# === PHASE 3: Error Handling & Edge Cases (4 tests) ===
# Hint: Finally, handle error conditions robustly

@pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not created yet")
class TestErrorHandling:
    """Phase 3: Handle errors and edge cases."""
    
    def test_raises_file_not_found(self):
        """Should raise FileNotFoundError for missing files.
        
        Hint: Don't catch FileNotFoundError - let it propagate naturally.
        """
        loader = CSVTransactionLoader()
        with pytest.raises(FileNotFoundError):
            loader.load('nonexistent_file.csv')
    
    def test_handles_empty_file(self, temp_csv_file):
        """Should handle empty file gracefully.
        
        Hint: Empty file can return empty list or raise ValueError.
        Either is acceptable.
        """
        with open(temp_csv_file, 'w') as f:
            f.write("")  # completely empty
        
        loader = CSVTransactionLoader()
        try:
            result = loader.load(temp_csv_file)
            assert result == []  # Empty list is fine
        except ValueError:
            pass  # ValueError is also acceptable
    
    def test_has_docstring(self):
        """CSVTransactionLoader should have a docstring.
        
        Hint: Add a class docstring explaining what the loader does.
        """
        assert CSVTransactionLoader.__doc__ is not None
        assert len(CSVTransactionLoader.__doc__.strip()) > 20
    
    def test_load_method_has_type_hints(self):
        """load() method should have type hints.
        
        Hint: Add type hints like:
        def load(self, filepath: str) -> List[Dict[str, Any]]:
        """
        import inspect
        sig = inspect.signature(CSVTransactionLoader.load)
        assert sig.return_annotation != inspect.Parameter.empty


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
