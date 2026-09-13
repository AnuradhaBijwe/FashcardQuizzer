"""
Unit tests for report factory.

Test coverage:
    - Creating registered report types
    - Invalid report type handling
    - Custom report registration
    - Available types listing
"""

import unittest

from expense_tracker.reports.report_factory import ReportFactory
from expense_tracker.reports.report_mode import (
    ReportMode,
    CategorySummaryReport,
    MonthlyTotalsReport,
    TopExpensesReport,
)
from expense_tracker.domain.exceptions import InvalidReportTypeError


class TestReportFactory(unittest.TestCase):
    """Test ReportFactory functionality."""

    def test_create_category_report(self):
        """Test creating CategorySummaryReport."""
        # TODO: Implement test
        pass

    def test_create_monthly_report(self):
        """Test creating MonthlyTotalsReport."""
        # TODO: Implement test
        pass

    def test_create_top_report(self):
        """Test creating TopExpensesReport."""
        # TODO: Implement test
        pass

    def test_create_top_report_with_custom_n(self):
        """Test creating TopExpensesReport with custom top_n."""
        # TODO: Implement test
        pass

    def test_create_invalid_report_raises_error(self):
        """Test that invalid report type raises InvalidReportTypeError."""
        # TODO: Implement test
        pass

    def test_get_available_types(self):
        """Test getting list of available report types."""
        # TODO: Implement test
        pass

    def test_register_custom_report(self):
        """Test registering a custom report type."""
        # TODO: Create a mock custom report class
        # TODO: Implement test
        pass

    def test_register_duplicate_name_raises_error(self):
        """Test that registering duplicate name raises ValueError."""
        # TODO: Implement test
        pass

    def test_register_non_reportmode_raises_error(self):
        """Test that registering non-ReportMode class raises TypeError."""
        # TODO: Implement test
        pass


if __name__ == '__main__':
    unittest.main()
