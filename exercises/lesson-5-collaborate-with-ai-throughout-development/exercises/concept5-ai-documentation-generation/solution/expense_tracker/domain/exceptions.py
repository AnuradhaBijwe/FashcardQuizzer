"""
Custom exceptions for expense tracker application.

This module defines domain-specific exceptions that provide clear error
context for different failure scenarios.
"""


class ExpenseTrackerError(Exception):
    """Base exception for all expense tracker errors."""
    pass


class DataLoadError(ExpenseTrackerError):
    """
    Raised when data cannot be loaded from source.

    Examples:
        - File not found
        - File cannot be read (permissions)
        - File is empty
    """
    pass


class ValidationError(ExpenseTrackerError):
    """
    Raised when data fails validation rules.

    Examples:
        - Invalid date format
        - Negative or zero amounts
        - Empty required fields
        - Invalid CSV structure
    """

    def __init__(self, message: str, row_number: int | None = None):
        """
        Initialize validation error.

        Args:
            message: Description of validation failure
            row_number: Optional row number where validation failed
        """
        self.row_number = row_number
        if row_number is not None:
            message = f"Row {row_number}: {message}"
        super().__init__(message)


class InvalidReportTypeError(ExpenseTrackerError):
    """
    Raised when an unknown report type is requested.

    Example:
        >>> raise InvalidReportTypeError('unknown_report', ['category', 'monthly'])
        InvalidReportTypeError: Unknown report type 'unknown_report'.
                                Available: category, monthly
    """

    def __init__(self, report_type: str, available_types: list[str]):
        """
        Initialize invalid report type error.

        Args:
            report_type: The invalid report type requested
            available_types: List of valid report type names
        """
        self.report_type = report_type
        self.available_types = available_types
        message = (
            f"Unknown report type '{report_type}'. "
            f"Available: {', '.join(available_types)}"
        )
        super().__init__(message)


class EmptyDatasetError(ExpenseTrackerError):
    """
    Raised when attempting to generate reports from empty transaction set.

    This can occur when:
        - No transactions loaded from file
        - All transactions filtered out by date/category
    """
    pass
