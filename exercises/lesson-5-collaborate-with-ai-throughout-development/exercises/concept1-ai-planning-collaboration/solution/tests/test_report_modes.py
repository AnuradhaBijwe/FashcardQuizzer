"""
Unit tests for report mode strategies.

Test coverage:
    - CategorySummaryReport aggregation and formatting
    - MonthlyTotalsReport grouping and formatting
    - TopExpensesReport sorting and limiting
    - Empty dataset handling
    - Edge cases (single transaction, same amounts, etc.)
"""

import unittest
from datetime import date
from decimal import Decimal

from expense_tracker.domain.models import Transaction
from expense_tracker.reports.report_mode import (
    CategorySummaryReport,
    MonthlyTotalsReport,
    TopExpensesReport,
)
from expense_tracker.domain.exceptions import EmptyDatasetError


class TestCategorySummaryReport(unittest.TestCase):
    """Test CategorySummaryReport strategy."""

    def setUp(self):
        """Set up test fixtures."""
        self.report = CategorySummaryReport()
        self.sample_transactions = [
            Transaction(date(2025, 1, 15), Decimal('42.50'), 'Food', 'Lunch'),
            Transaction(date(2025, 1, 16), Decimal('120.00'), 'Transport', 'Metro'),
            Transaction(date(2025, 1, 17), Decimal('35.00'), 'Food', 'Groceries'),
        ]

    def test_process_transactions_groups_by_category(self):
        """Test that transactions are grouped by category correctly."""
        # TODO: Implement test
        # Verify Food total is $77.50, Transport is $120.00
        pass

    def test_process_empty_transactions_raises_error(self):
        """Test that empty transaction list raises EmptyDatasetError."""
        # TODO: Implement test
        pass

    def test_get_report_name(self):
        """Test that report name is returned correctly."""
        # TODO: Implement test
        pass

    def test_output_format_has_headers(self):
        """Test that output includes proper headers."""
        # TODO: Implement test
        pass

    def test_categories_sorted_by_total(self):
        """Test that categories are sorted by total amount descending."""
        # TODO: Implement test
        pass


class TestMonthlyTotalsReport(unittest.TestCase):
    """Test MonthlyTotalsReport strategy."""

    def setUp(self):
        """Set up test fixtures."""
        self.report = MonthlyTotalsReport()
        self.sample_transactions = [
            Transaction(date(2025, 1, 15), Decimal('100.00'), 'Food', 'Jan expense'),
            Transaction(date(2025, 2, 16), Decimal('200.00'), 'Transport', 'Feb expense'),
            Transaction(date(2025, 1, 20), Decimal('50.00'), 'Food', 'Another Jan'),
        ]

    def test_process_transactions_groups_by_month(self):
        """Test that transactions are grouped by month correctly."""
        # TODO: Implement test
        # Verify Jan total is $150.00, Feb is $200.00
        pass

    def test_process_empty_transactions_raises_error(self):
        """Test that empty transaction list raises EmptyDatasetError."""
        # TODO: Implement test
        pass

    def test_months_sorted_chronologically(self):
        """Test that months are sorted in chronological order."""
        # TODO: Implement test
        pass


class TestTopExpensesReport(unittest.TestCase):
    """Test TopExpensesReport strategy."""

    def setUp(self):
        """Set up test fixtures."""
        self.report = TopExpensesReport(top_n=3)
        self.sample_transactions = [
            Transaction(date(2025, 1, 15), Decimal('50.00'), 'Food', 'Expense 1'),
            Transaction(date(2025, 1, 16), Decimal('200.00'), 'Transport', 'Expense 2'),
            Transaction(date(2025, 1, 17), Decimal('100.00'), 'Food', 'Expense 3'),
            Transaction(date(2025, 1, 18), Decimal('75.00'), 'Utilities', 'Expense 4'),
        ]

    def test_process_transactions_shows_top_n(self):
        """Test that only top N expenses are shown."""
        # TODO: Implement test
        # Verify only 3 transactions shown: $200, $100, $75
        pass

    def test_top_expenses_sorted_by_amount(self):
        """Test that expenses are sorted by amount descending."""
        # TODO: Implement test
        pass

    def test_process_fewer_than_n_transactions(self):
        """Test handling when there are fewer transactions than top_n."""
        # TODO: Implement test with only 2 transactions for top_n=3
        pass

    def test_invalid_top_n_raises_error(self):
        """Test that invalid top_n values raise ValueError."""
        # TODO: Implement test for top_n=0, top_n=-1
        pass

    def test_get_report_name_includes_n(self):
        """Test that report name includes the top_n value."""
        # TODO: Implement test
        pass


if __name__ == '__main__':
    unittest.main()
