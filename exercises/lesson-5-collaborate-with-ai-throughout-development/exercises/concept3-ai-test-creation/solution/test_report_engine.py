"""
Comprehensive pytest test suite for ReportEngine class.

This test suite covers:
1. Basic Functionality - initialization and basic operations
2. Happy Path Scenarios - successful report generation with valid data
3. Error Handling - FileNotFoundError, ValueError, empty datasets
4. Edge Cases - single transaction, large datasets, special characters

Test Quality Features:
- Uses pytest fixtures for reusable test data
- Mocks external dependencies (TransactionLoader, ReportMode)
- Clear test names describing what's being tested
- Arrange-Act-Assert structure
- Each test focuses on ONE behavior
- Parametrized tests for similar scenarios
"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import date
from decimal import Decimal

from report_engine import ReportEngine


# ===== FIXTURES =====

@pytest.fixture
def sample_transactions():
    """
    Fixture providing sample transaction data for testing.

    Returns a list of transaction dictionaries with realistic test data.
    This avoids repeating test data setup across multiple tests.
    """
    return [
        {
            'date': date(2025, 1, 15),
            'amount': Decimal('42.50'),
            'category': 'Food',
            'description': 'Lunch at cafe'
        },
        {
            'date': date(2025, 1, 16),
            'amount': Decimal('120.00'),
            'category': 'Transport',
            'description': 'Monthly metro pass'
        },
        {
            'date': date(2025, 1, 17),
            'amount': Decimal('35.75'),
            'category': 'Food',
            'description': 'Groceries'
        }
    ]


@pytest.fixture
def single_transaction():
    """Fixture providing a single transaction for edge case testing."""
    return [
        {
            'date': date(2025, 1, 15),
            'amount': Decimal('99.99'),
            'category': 'Shopping',
            'description': 'Single purchase'
        }
    ]


@pytest.fixture
def large_transaction_set():
    """
    Fixture providing a large set of transactions for performance testing.

    Simulates processing of 1000+ transactions to test scalability.
    """
    transactions = []
    for i in range(1000):
        transactions.append({
            'date': date(2025, 1, (i % 28) + 1),
            'amount': Decimal(f'{(i % 500) + 10}.{i % 100:02d}'),
            'category': f'Category_{i % 10}',
            'description': f'Transaction {i}'
        })
    return transactions


@pytest.fixture
def transactions_with_special_chars():
    """Fixture providing transactions with special characters in descriptions."""
    return [
        {
            'date': date(2025, 1, 15),
            'amount': Decimal('25.00'),
            'category': 'Food & Dining',
            'description': 'Coffee @ "Joe\'s Café" <downtown>'
        },
        {
            'date': date(2025, 1, 16),
            'amount': Decimal('50.00'),
            'category': 'Entertainment',
            'description': 'Movie: "The Matrix" (2hrs)'
        }
    ]


@pytest.fixture
def mock_loader():
    """
    Fixture providing a mock TransactionLoader.

    This allows testing ReportEngine in isolation without needing
    a real loader implementation or actual CSV files.
    """
    loader = Mock()
    return loader


@pytest.fixture
def mock_mode():
    """
    Fixture providing a mock ReportMode strategy.

    This allows testing ReportEngine without needing real report
    mode implementations.
    """
    mode = Mock()
    return mode


@pytest.fixture
def report_engine(mock_loader):
    """
    Fixture providing a ReportEngine instance with mock loader.

    This reduces boilerplate in tests that need a basic engine instance.
    """
    return ReportEngine(mock_loader)


# ===== TEST CLASS: Basic Functionality =====

class TestReportEngineBasics:
    """
    Test basic ReportEngine functionality.

    Covers:
    - Initialization
    - Basic attribute access
    - Simple successful operations
    """

    def test_initialization_with_loader(self, mock_loader):
        """Test that ReportEngine can be initialized with a loader."""
        # Act
        engine = ReportEngine(mock_loader)

        # Assert
        assert engine is not None, "ReportEngine instance should be created"
        assert engine.loader is mock_loader, "Loader should be stored in instance"

    def test_loader_attribute_accessible(self, report_engine, mock_loader):
        """Test that loader attribute is accessible after initialization."""
        # Assert
        assert hasattr(report_engine, 'loader'), "Engine should have loader attribute"
        assert report_engine.loader is mock_loader, "Loader should be accessible"

    def test_generate_report_method_exists(self, report_engine):
        """Test that generate_report method exists and is callable."""
        # Assert
        assert hasattr(report_engine, 'generate_report'), "Should have generate_report method"
        assert callable(report_engine.generate_report), "generate_report should be callable"

    def test_generate_report_returns_dict(self, report_engine, mock_loader, mock_mode, sample_transactions):
        """Test that generate_report returns a dictionary."""
        # Arrange
        mock_loader.load.return_value = sample_transactions
        mock_mode.process_transactions.return_value = {'total': 198.25}

        # Act
        result = report_engine.generate_report('test.csv', mock_mode)

        # Assert
        assert isinstance(result, dict), "Result should be a dictionary"


# ===== TEST CLASS: Happy Path Scenarios =====

class TestReportGenerationHappyPath:
    """
    Test successful report generation scenarios.

    Covers:
    - Multiple transactions
    - Different report modes
    - Correct data flow through components
    """

    def test_successful_report_generation_with_valid_data(
        self, report_engine, mock_loader, mock_mode, sample_transactions
    ):
        """Test successful report generation with valid transaction data."""
        # Arrange
        expected_report = {
            'mode': 'summary',
            'total': Decimal('198.25'),
            'count': 3
        }
        mock_loader.load.return_value = sample_transactions
        mock_mode.process_transactions.return_value = expected_report

        # Act
        result = report_engine.generate_report('expenses.csv', mock_mode)

        # Assert
        assert result == expected_report, "Should return expected report data"
        assert result['total'] == Decimal('198.25'), "Total should match expected value"
        assert result['count'] == 3, "Count should match number of transactions"

    def test_loader_called_with_correct_filepath(
        self, report_engine, mock_loader, mock_mode, sample_transactions
    ):
        """Test that loader.load is called with the correct filepath."""
        # Arrange
        filepath = '/path/to/transactions.csv'
        mock_loader.load.return_value = sample_transactions
        mock_mode.process_transactions.return_value = {}

        # Act
        report_engine.generate_report(filepath, mock_mode)

        # Assert
        mock_loader.load.assert_called_once_with(filepath), \
            "Loader should be called once with correct filepath"

    def test_mode_receives_transactions_from_loader(
        self, report_engine, mock_loader, mock_mode, sample_transactions
    ):
        """Test that mode.process_transactions receives data from loader."""
        # Arrange
        mock_loader.load.return_value = sample_transactions
        mock_mode.process_transactions.return_value = {}

        # Act
        report_engine.generate_report('test.csv', mock_mode)

        # Assert
        mock_mode.process_transactions.assert_called_once_with(sample_transactions), \
            "Mode should receive transactions from loader"

    @pytest.mark.parametrize("mode_name,expected_output", [
        ('summary', {'type': 'summary', 'data': {'Food': 78.25}}),
        ('monthly', {'type': 'monthly', 'data': {'2025-01': 198.25}}),
        ('top', {'type': 'top', 'transactions': []}),
    ])
    def test_different_report_modes(
        self, report_engine, mock_loader, sample_transactions, mode_name, expected_output
    ):
        """
        Test that ReportEngine works with different report modes.

        Uses parametrize to test multiple mode types without code duplication.
        """
        # Arrange
        mock_loader.load.return_value = sample_transactions
        mock_mode = Mock()
        mock_mode.process_transactions.return_value = expected_output

        # Act
        result = report_engine.generate_report('test.csv', mock_mode)

        # Assert
        assert result['type'] == expected_output['type'], \
            f"Should handle {mode_name} mode correctly"

    def test_multiple_reports_with_same_engine(
        self, report_engine, mock_loader, mock_mode, sample_transactions
    ):
        """Test that the same engine instance can generate multiple reports."""
        # Arrange
        mock_loader.load.return_value = sample_transactions
        mock_mode.process_transactions.return_value = {'total': 100}

        # Act
        result1 = report_engine.generate_report('file1.csv', mock_mode)
        result2 = report_engine.generate_report('file2.csv', mock_mode)

        # Assert
        assert result1 == result2, "Should produce consistent results"
        assert mock_loader.load.call_count == 2, "Loader should be called for each report"
        assert mock_mode.process_transactions.call_count == 2, \
            "Mode should be called for each report"

    def test_report_generation_workflow_order(
        self, report_engine, mock_loader, mock_mode, sample_transactions
    ):
        """Test that workflow steps happen in correct order: load then process."""
        # Arrange
        call_order = []

        def record_load(*args):
            call_order.append('load')
            return sample_transactions

        def record_process(*args):
            call_order.append('process')
            return {}

        mock_loader.load.side_effect = record_load
        mock_mode.process_transactions.side_effect = record_process

        # Act
        report_engine.generate_report('test.csv', mock_mode)

        # Assert
        assert call_order == ['load', 'process'], \
            "Should load transactions before processing"


# ===== TEST CLASS: Error Handling =====

class TestReportGenerationErrors:
    """
    Test error handling in report generation.

    Covers:
    - FileNotFoundError from loader
    - ValueError from invalid data
    - Empty transaction lists
    - Loader failures
    - Loader returning None instead of list
    - Unexpected exceptions from mode processing
    """

    def test_file_not_found_error_propagates(self, report_engine, mock_loader, mock_mode):
        """Test that FileNotFoundError from loader is propagated."""
        # Arrange
        mock_loader.load.side_effect = FileNotFoundError("File not found: missing.csv")

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            report_engine.generate_report('missing.csv', mock_mode)

        assert "missing.csv" in str(exc_info.value), \
            "Error message should include filename"
        mock_mode.process_transactions.assert_not_called(), \
            "Mode should not be called when loader fails"

    def test_file_not_found_specific_message(self, report_engine, mock_loader, mock_mode):
        """Test that FileNotFoundError contains specific error message."""
        # Arrange
        error_message = "File not found: /path/to/nonexistent.csv"
        mock_loader.load.side_effect = FileNotFoundError(error_message)

        # Act & Assert
        with pytest.raises(FileNotFoundError, match="nonexistent.csv"):
            report_engine.generate_report('/path/to/nonexistent.csv', mock_mode)

    def test_value_error_from_invalid_csv_propagates(
        self, report_engine, mock_loader, mock_mode
    ):
        """Test that ValueError from invalid CSV data is propagated."""
        # Arrange
        mock_loader.load.side_effect = ValueError("Invalid CSV format: missing columns")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            report_engine.generate_report('invalid.csv', mock_mode)

        assert "Invalid CSV" in str(exc_info.value), \
            "Error message should indicate CSV problem"

    def test_value_error_from_mode_processing_propagates(
        self, report_engine, mock_loader, mock_mode, sample_transactions
    ):
        """Test that ValueError from mode processing is propagated."""
        # Arrange
        mock_loader.load.return_value = sample_transactions
        mock_mode.process_transactions.side_effect = ValueError("Cannot process invalid data")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            report_engine.generate_report('test.csv', mock_mode)

        assert "Cannot process" in str(exc_info.value), \
            "Error message from mode should be preserved"

    def test_empty_transaction_list_handling(self, report_engine, mock_loader, mock_mode):
        """Test handling of empty transaction list from loader."""
        # Arrange
        mock_loader.load.return_value = []
        mock_mode.process_transactions.return_value = {'total': 0, 'count': 0}

        # Act
        result = report_engine.generate_report('empty.csv', mock_mode)

        # Assert
        mock_mode.process_transactions.assert_called_once_with([]), \
            "Mode should still be called with empty list"
        assert result['count'] == 0, "Should return zero count for empty dataset"

    def test_loader_raises_permission_error(self, report_engine, mock_loader, mock_mode):
        """Test that permission errors from loader are propagated."""
        # Arrange
        mock_loader.load.side_effect = PermissionError("Permission denied")

        # Act & Assert
        with pytest.raises(PermissionError):
            report_engine.generate_report('restricted.csv', mock_mode)

    def test_loader_raises_generic_exception(self, report_engine, mock_loader, mock_mode):
        """Test that unexpected exceptions from loader are propagated."""
        # Arrange
        mock_loader.load.side_effect = RuntimeError("Unexpected error")

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            report_engine.generate_report('test.csv', mock_mode)

        assert "Unexpected error" in str(exc_info.value)

    def test_mode_not_called_when_loader_fails(self, report_engine, mock_loader, mock_mode):
        """Test that mode is not called when loader fails."""
        # Arrange
        mock_loader.load.side_effect = FileNotFoundError("File not found")

        # Act
        try:
            report_engine.generate_report('missing.csv', mock_mode)
        except FileNotFoundError:
            pass

        # Assert
        mock_mode.process_transactions.assert_not_called(), \
            "Mode should not be called if loader fails"

    def test_loader_returns_none_instead_of_list(self, report_engine, mock_loader, mock_mode):
        """
        Test that TypeError is raised when loader returns None instead of list.

        This critical edge case catches bugs in loader implementations where
        None is returned instead of an empty list or raising an exception.
        The error should occur when mode tries to iterate over None, which
        real ReportMode implementations would do.
        """
        # Arrange
        mock_loader.load.return_value = None

        # Configure mock to behave like real mode: raise TypeError when given None
        def process_with_validation(transactions):
            if transactions is None:
                raise TypeError("'NoneType' object is not iterable")
            return {'count': len(transactions)}

        mock_mode.process_transactions.side_effect = process_with_validation

        # Act & Assert
        with pytest.raises(TypeError) as exc_info:
            report_engine.generate_report('test.csv', mock_mode)

        # Verify the error message indicates the problem
        assert "NoneType" in str(exc_info.value) or "not iterable" in str(exc_info.value), \
            "Error message should indicate None cannot be iterated"

        # Verify loader was called before failure
        mock_loader.load.assert_called_once_with('test.csv'), \
            "Loader should have been called"
        # Mode was also called (with None), which caused the error
        mock_mode.process_transactions.assert_called_once_with(None), \
            "Mode should have been called with None, causing the error"

    def test_mode_raises_unexpected_exception(
        self, report_engine, mock_loader, mock_mode, sample_transactions
    ):
        """
        Test that unexpected exceptions from mode.process_transactions are propagated.

        This tests the error handling when the report mode encounters an
        unexpected error during processing (e.g., division by zero, attribute
        error, index error). These exceptions should propagate up with their
        original context preserved for debugging.
        """
        # Arrange
        mock_loader.load.return_value = sample_transactions

        # Simulate unexpected exception during processing
        unexpected_error = ZeroDivisionError("division by zero in report calculation")
        mock_mode.process_transactions.side_effect = unexpected_error

        # Act & Assert
        with pytest.raises(ZeroDivisionError) as exc_info:
            report_engine.generate_report('test.csv', mock_mode)

        # Verify the original exception is preserved
        assert "division by zero" in str(exc_info.value), \
            "Original exception message should be preserved"

        # Verify both loader and mode were called before failure
        mock_loader.load.assert_called_once_with('test.csv'), \
            "Loader should have been called"
        mock_mode.process_transactions.assert_called_once_with(sample_transactions), \
            "Mode should have been called with loaded transactions"


# ===== TEST CLASS: Edge Cases =====

class TestEdgeCases:
    """
    Test edge cases in report generation.

    Covers:
    - Single transaction
    - Very large transaction lists (1000+ items)
    - Special characters in data
    - Unusual but valid inputs
    """

    def test_single_transaction(
        self, report_engine, mock_loader, mock_mode, single_transaction
    ):
        """Test report generation with a single transaction."""
        # Arrange
        mock_loader.load.return_value = single_transaction
        expected_report = {'total': Decimal('99.99'), 'count': 1}
        mock_mode.process_transactions.return_value = expected_report

        # Act
        result = report_engine.generate_report('single.csv', mock_mode)

        # Assert
        assert result['count'] == 1, "Should handle single transaction"
        assert result['total'] == Decimal('99.99'), "Should calculate correct total"
        mock_mode.process_transactions.assert_called_once_with(single_transaction)

    def test_very_large_transaction_list(
        self, report_engine, mock_loader, mock_mode, large_transaction_set
    ):
        """Test report generation with 1000+ transactions."""
        # Arrange
        mock_loader.load.return_value = large_transaction_set
        expected_report = {'count': len(large_transaction_set)}
        mock_mode.process_transactions.return_value = expected_report

        # Act
        result = report_engine.generate_report('large.csv', mock_mode)

        # Assert
        assert result['count'] == 1000, "Should handle large dataset"
        mock_mode.process_transactions.assert_called_once()
        call_args = mock_mode.process_transactions.call_args[0][0]
        assert len(call_args) == 1000, "Should pass all transactions to mode"

    def test_special_characters_in_transaction_data(
        self, report_engine, mock_loader, mock_mode, transactions_with_special_chars
    ):
        """Test handling of special characters in transaction descriptions."""
        # Arrange
        mock_loader.load.return_value = transactions_with_special_chars
        mock_mode.process_transactions.return_value = {'count': 2}

        # Act
        result = report_engine.generate_report('special.csv', mock_mode)

        # Assert
        assert result['count'] == 2, "Should handle special characters"
        call_args = mock_mode.process_transactions.call_args[0][0]
        assert 'Coffee @ "Joe\'s Café"' in call_args[0]['description'], \
            "Special characters should be preserved"

    def test_transactions_with_unicode_characters(self, report_engine, mock_loader, mock_mode):
        """Test handling of Unicode characters in transaction data."""
        # Arrange
        unicode_transactions = [
            {
                'date': date(2025, 1, 15),
                'amount': Decimal('50.00'),
                'category': 'Food',
                'description': 'Café français 🇫🇷'
            }
        ]
        mock_loader.load.return_value = unicode_transactions
        mock_mode.process_transactions.return_value = {'count': 1}

        # Act
        result = report_engine.generate_report('unicode.csv', mock_mode)

        # Assert
        assert result['count'] == 1, "Should handle Unicode characters"
        call_args = mock_mode.process_transactions.call_args[0][0]
        assert '🇫🇷' in call_args[0]['description'], "Unicode emoji should be preserved"

    def test_transactions_with_maximum_decimal_precision(
        self, report_engine, mock_loader, mock_mode
    ):
        """Test handling of decimal amounts with high precision."""
        # Arrange
        precise_transactions = [
            {
                'date': date(2025, 1, 15),
                'amount': Decimal('99.999999'),
                'category': 'Test',
                'description': 'Precise amount'
            }
        ]
        mock_loader.load.return_value = precise_transactions
        mock_mode.process_transactions.return_value = {'total': Decimal('99.999999')}

        # Act
        result = report_engine.generate_report('precise.csv', mock_mode)

        # Assert
        assert result['total'] == Decimal('99.999999'), \
            "Should preserve decimal precision"

    def test_filepath_with_special_characters(
        self, report_engine, mock_loader, mock_mode, sample_transactions
    ):
        """Test that filepaths with special characters are passed correctly to loader."""
        # Arrange
        special_path = '/path/with spaces/file-name_123.csv'
        mock_loader.load.return_value = sample_transactions
        mock_mode.process_transactions.return_value = {}

        # Act
        report_engine.generate_report(special_path, mock_mode)

        # Assert
        mock_loader.load.assert_called_once_with(special_path), \
            "Should pass special filepath unchanged to loader"

    def test_different_date_ranges_in_transactions(
        self, report_engine, mock_loader, mock_mode
    ):
        """Test handling of transactions across different date ranges."""
        # Arrange
        multi_year_transactions = [
            {
                'date': date(2024, 1, 1),
                'amount': Decimal('100.00'),
                'category': 'Food',
                'description': 'Old transaction'
            },
            {
                'date': date(2025, 12, 31),
                'amount': Decimal('200.00'),
                'category': 'Food',
                'description': 'Recent transaction'
            }
        ]
        mock_loader.load.return_value = multi_year_transactions
        mock_mode.process_transactions.return_value = {'count': 2}

        # Act
        result = report_engine.generate_report('multi_year.csv', mock_mode)

        # Assert
        assert result['count'] == 2, "Should handle transactions across date ranges"
        call_args = mock_mode.process_transactions.call_args[0][0]
        assert call_args[0]['date'] == date(2024, 1, 1), "Should preserve date order"
        assert call_args[1]['date'] == date(2025, 12, 31)
