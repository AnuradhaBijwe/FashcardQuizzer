"""
Streamlined tests for ReportMode strategy implementations.
Reduced from 21 to 12 essential tests with better organization.

Tests cover both strategy implementations with clear progression.
"""
import pytest

# Students will create this module
try:
    from report_modes import SummaryByCategory, MonthlyTotalReport
    IMPLEMENTATION_EXISTS = True
except ImportError:
    IMPLEMENTATION_EXISTS = False
    SummaryByCategory = None
    MonthlyTotalReport = None


@pytest.fixture
def sample_transactions():
    """Sample transactions for testing."""
    return [
        {'date': '2024-01-15', 'amount': 45.50, 'category': 'Food', 'description': 'Grocery'},
        {'date': '2024-01-16', 'amount': 120.00, 'category': 'Transport', 'description': 'Gas'},
        {'date': '2024-01-17', 'amount': 25.99, 'category': 'Food', 'description': 'Restaurant'},
        {'date': '2024-02-10', 'amount': 75.00, 'category': 'Entertainment', 'description': 'Concert'},
        {'date': '2024-02-15', 'amount': 30.00, 'category': 'Food', 'description': 'Lunch'},
    ]


# === SUMMARY BY CATEGORY TESTS (6 tests) ===

@pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not created yet")
class TestSummaryByCategory:
    """Test SummaryByCategory strategy implementation."""
    
    def test_can_instantiate(self):
        """Should be able to create SummaryByCategory instance.
        
        Hint: Create a class that implements the ReportMode interface.
        """
        strategy = SummaryByCategory()
        assert strategy is not None
    
    def test_groups_transactions_by_category(self, sample_transactions):
        """Should group transactions by category and sum amounts.
        
        Hint: Use a dictionary or defaultdict to accumulate amounts by category.
        Expected: Food=101.49, Transport=120.00, Entertainment=75.00
        """
        strategy = SummaryByCategory()
        result = strategy.process_transactions(sample_transactions)
        
        assert 'data' in result
        data = result['data']
        
        # Check Food category (45.50 + 25.99 + 30.00)
        assert 'Food' in data
        assert abs(data['Food'] - 101.49) < 0.01
        
        # Check Transport category
        assert 'Transport' in data
        assert data['Transport'] == 120.00
    
    def test_calculates_total(self, sample_transactions):
        """Result should include overall total.
        
        Hint: Sum all amounts regardless of category.
        """
        strategy = SummaryByCategory()
        result = strategy.process_transactions(sample_transactions)
        
        assert 'total' in result
        expected_total = sum(t['amount'] for t in sample_transactions)
        assert abs(result['total'] - expected_total) < 0.01
    
    def test_handles_empty_transactions(self):
        """Should handle empty transaction list.
        
        Hint: Return empty data dict and total of 0.0
        """
        strategy = SummaryByCategory()
        result = strategy.process_transactions([])
        
        assert result['data'] == {}
        assert result['total'] == 0.0
    
    def test_result_has_mode_identifier(self, sample_transactions):
        """Result should include mode identifier.
        
        Hint: Include a 'mode' key in the result dict.
        """
        strategy = SummaryByCategory()
        result = strategy.process_transactions(sample_transactions)
        
        assert 'mode' in result
    
    def test_has_docstring(self):
        """SummaryByCategory should have docstring."""
        assert SummaryByCategory.__doc__ is not None
        assert len(SummaryByCategory.__doc__.strip()) > 20


# === MONTHLY TOTAL REPORT TESTS (6 tests) ===

@pytest.mark.skipif(not IMPLEMENTATION_EXISTS, reason="Implementation not created yet")
class TestMonthlyTotalReport:
    """Test MonthlyTotalReport strategy implementation."""
    
    def test_can_instantiate(self):
        """Should be able to create MonthlyTotalReport instance."""
        strategy = MonthlyTotalReport()
        assert strategy is not None
    
    def test_groups_transactions_by_month(self, sample_transactions):
        """Should group transactions by month and sum amounts.
        
        Hint: Extract year-month from date field (YYYY-MM-DD -> YYYY-MM)
        Use date_str[:7] to get first 7 characters.
        Expected: 2024-01=191.49, 2024-02=105.00
        """
        strategy = MonthlyTotalReport()
        result = strategy.process_transactions(sample_transactions)
        
        assert 'data' in result
        data = result['data']
        
        # Check January (45.50 + 120.00 + 25.99)
        assert '2024-01' in data
        assert abs(data['2024-01'] - 191.49) < 0.01
        
        # Check February (75.00 + 30.00)
        assert '2024-02' in data
        assert abs(data['2024-02'] - 105.00) < 0.01
    
    def test_calculates_total(self, sample_transactions):
        """Result should include overall total."""
        strategy = MonthlyTotalReport()
        result = strategy.process_transactions(sample_transactions)
        
        assert 'total' in result
        expected_total = sum(t['amount'] for t in sample_transactions)
        assert abs(result['total'] - expected_total) < 0.01
    
    def test_handles_empty_transactions(self):
        """Should handle empty transaction list."""
        strategy = MonthlyTotalReport()
        result = strategy.process_transactions([])
        
        assert result['data'] == {}
        assert result['total'] == 0.0
    
    def test_month_keys_correctly_formatted(self, sample_transactions):
        """Month keys should be in YYYY-MM format.
        
        Hint: All keys in data dict should be 7 characters long (YYYY-MM).
        """
        strategy = MonthlyTotalReport()
        result = strategy.process_transactions(sample_transactions)
        
        for month_key in result['data'].keys():
            assert len(month_key) == 7
            assert month_key[4] == '-'  # Format: YYYY-MM
    
    def test_has_docstring(self):
        """MonthlyTotalReport should have docstring."""
        assert MonthlyTotalReport.__doc__ is not None
        assert len(MonthlyTotalReport.__doc__.strip()) > 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
