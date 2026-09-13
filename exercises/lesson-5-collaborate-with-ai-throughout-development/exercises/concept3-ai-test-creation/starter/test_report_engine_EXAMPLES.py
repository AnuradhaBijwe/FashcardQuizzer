"""
EXAMPLE TESTS for ReportEngine

These are example tests showing good test structure and patterns.
Use these as a template when creating your own test_report_engine.py file.

Students: Study these examples, then create test_report_engine.py with YOUR tests.
"""
import pytest
from unittest.mock import Mock
from report_engine import ReportEngine


@pytest.fixture
def mock_loader():
    """Example fixture: Create a mock TransactionLoader.
    
    Fixtures make test setup reusable across multiple tests.
    This avoids repeating the same setup code.
    """
    loader = Mock()
    return loader


@pytest.fixture
def sample_transactions():
    """Example fixture: Provide sample test data.
    
    Using fixtures for test data makes tests more readable
    and easier to maintain.
    """
    return [
        {'date': '2024-01-15', 'amount': 45.50, 'category': 'Food'},
        {'date': '2024-01-16', 'amount': 120.00, 'category': 'Transport'},
    ]


class TestReportEngineExamples:
    """Example test class showing good test structure."""
    
    def test_example_basic_instantiation(self, mock_loader):
        """Example: Test that you can create a ReportEngine.
        
        This is a simple "smoke test" - it checks that the basic
        structure works before testing more complex behavior.
        
        Pattern:
        1. Arrange: Set up your test objects
        2. Act: Do the thing you're testing  
        3. Assert: Check the result is correct
        """
        # Arrange - mock_loader provided by fixture
        
        # Act
        engine = ReportEngine(mock_loader)
        
        # Assert
        assert engine is not None
        assert engine.loader is mock_loader
    
    def test_example_successful_report_generation(self, mock_loader, sample_transactions):
        """Example: Test successful report generation with mocks.
        
        This shows how to:
        - Set up mock return values
        - Test the happy path
        - Verify mocks were called correctly
        
        Mocking lets us test ReportEngine in isolation without
        needing real TransactionLoader or ReportMode implementations.
        """
        # Arrange
        mock_loader.load.return_value = sample_transactions
        
        mock_mode = Mock()
        mock_mode.process_transactions.return_value = {
            'mode': 'summary',
            'data': {'Food': 45.50, 'Transport': 120.00},
            'total': 165.50
        }
        
        engine = ReportEngine(mock_loader)
        
        # Act
        result = engine.generate_report('test.csv', mock_mode)
        
        # Assert - check the result
        assert result['mode'] == 'summary'
        assert result['total'] == 165.50
        
        # Assert - verify mocks were called correctly
        mock_loader.load.assert_called_once_with('test.csv')
        mock_mode.process_transactions.assert_called_once_with(sample_transactions)
    
    def test_example_error_handling(self, mock_loader):
        """Example: Test that errors are handled correctly.
        
        This shows how to test error conditions using pytest.raises().
        Good tests cover both success AND failure cases.
        """
        # Arrange - make the mock raise an exception
        mock_loader.load.side_effect = FileNotFoundError("File not found")
        
        engine = ReportEngine(mock_loader)
        mock_mode = Mock()
        
        # Act & Assert - use pytest.raises to check exception is raised
        with pytest.raises(FileNotFoundError):
            engine.generate_report('missing.csv', mock_mode)
        
        # Additional assert - verify mode was NOT called when loader failed
        mock_mode.process_transactions.assert_not_called()


# === INSTRUCTIONS FOR STUDENTS ===
"""
Now it's your turn! Create test_report_engine.py with YOUR tests.

You should test:

1. Basic functionality:
   - Can instantiate ReportEngine
   - Can generate reports successfully
   - Returns correct data structure

2. Error handling:
   - File not found errors
   - Invalid data errors
   - Empty transaction lists

3. Integration scenarios:
   - Complete flow from file to report
   - Multiple reports with same engine
   - Different modes with same data

Remember to:
- Use fixtures for reusable setup (mock_loader, sample_transactions, etc.)
- Use mocks to isolate ReportEngine from dependencies
- Write clear, descriptive test names
- Include docstrings explaining what each test does
- Test behavior, not implementation details

Run validation when done:
    pytest validate_test_quality.py -v
"""
