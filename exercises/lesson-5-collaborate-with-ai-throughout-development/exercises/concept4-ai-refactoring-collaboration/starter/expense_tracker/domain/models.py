"""
Domain models for expense tracker application.

This module contains core data structures representing the business domain.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Transaction:
    """
    Immutable representation of a financial transaction.

    Attributes:
        date: Transaction date
        amount: Transaction amount (positive for expenses)
        category: Expense category (e.g., 'Food', 'Transportation')
        description: Human-readable transaction description

    Example:
        >>> tx = Transaction(
        ...     date=date(2025, 1, 15),
        ...     amount=Decimal('42.50'),
        ...     category='Food',
        ...     description='Lunch at cafe'
        ... )
    """
    date: date
    amount: Decimal
    category: str
    description: str

    def __post_init__(self) -> None:
        """
        Validate transaction data after initialization.

        Raises:
            ValueError: If amount is negative or zero
            ValueError: If category or description is empty
        """
        if self.amount <= 0:
            raise ValueError(f"Amount must be positive, got {self.amount}")

        if not self.category or not self.category.strip():
            raise ValueError("Category cannot be empty")

        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")


@dataclass(frozen=True)
class ValidationResult:
    """
    Result of data validation operation.

    Attributes:
        is_valid: Whether validation passed
        errors: List of validation error messages (empty if valid)
        row_number: Optional row number for CSV validation context

    Example:
        >>> result = ValidationResult(
        ...     is_valid=False,
        ...     errors=['Invalid date format'],
        ...     row_number=5
        ... )
    """
    is_valid: bool
    errors: list[str]
    row_number: Optional[int] = None

    @classmethod
    def success(cls) -> 'ValidationResult':
        """Create a successful validation result."""
        return cls(is_valid=True, errors=[])

    @classmethod
    def failure(cls, *errors: str, row_number: Optional[int] = None) -> 'ValidationResult':
        """
        Create a failed validation result.

        Args:
            *errors: Variable number of error messages
            row_number: Optional row number for context

        Returns:
            ValidationResult with is_valid=False
        """
        return cls(is_valid=False, errors=list(errors), row_number=row_number)
