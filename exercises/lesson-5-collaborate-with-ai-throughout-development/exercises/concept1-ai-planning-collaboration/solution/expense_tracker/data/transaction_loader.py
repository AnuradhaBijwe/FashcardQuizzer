"""
Abstract interface for loading transaction data.

This module defines the contract for loading transactions from various sources
(CSV files, databases, APIs, etc.) while ensuring validation and error handling.
"""

import csv
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import List

from expense_tracker.domain.models import Transaction
from expense_tracker.domain.exceptions import DataLoadError, ValidationError


class TransactionLoader(ABC):
    """
    Abstract base class for loading and validating transaction data.

    This interface follows the Open/Closed Principle - new data sources can be
    added by creating new implementations without modifying existing code.

    Implementations must:
        1. Load data from source (file, database, API, etc.)
        2. Validate each transaction against business rules
        3. Convert raw data into Transaction objects
        4. Handle errors with appropriate exceptions

    Example implementation:
        >>> class CSVTransactionLoader(TransactionLoader):
        ...     def load(self, source: str) -> List[Transaction]:
        ...         # Read CSV file, parse rows, return transactions
        ...         pass
    """

    @abstractmethod
    def load(self, source: str) -> List[Transaction]:
        """
        Load transactions from specified source.

        This method is responsible for:
            - Opening/connecting to the data source
            - Reading and parsing data
            - Validating each record
            - Creating Transaction objects
            - Closing resources (file handles, connections)

        Args:
            source: Path or identifier for the data source.
                   For file-based loaders: absolute or relative file path
                   For database loaders: connection string or table name
                   For API loaders: endpoint URL

        Returns:
            List of validated Transaction objects in order of appearance.
            Returns empty list if source contains no valid transactions.

        Raises:
            DataLoadError: When source cannot be accessed or read.
                Examples:
                    - File not found
                    - Permission denied
                    - Network connection failure
                    - Empty file

            ValidationError: When data fails validation rules.
                Examples:
                    - Invalid date format (must be ISO 8601: YYYY-MM-DD)
                    - Invalid amount (must be positive decimal)
                    - Missing required fields (date, amount, category, description)
                    - Invalid CSV structure (wrong number of columns)

                Note: Include row_number in ValidationError for easier debugging

        Example:
            >>> loader = CSVTransactionLoader()
            >>> transactions = loader.load('expenses.csv')
            >>> print(f"Loaded {len(transactions)} transactions")
            Loaded 150 transactions

            >>> # Error handling
            >>> try:
            ...     transactions = loader.load('missing.csv')
            ... except DataLoadError as e:
            ...     print(f"Cannot load data: {e}")
            ... except ValidationError as e:
            ...     print(f"Invalid data at row {e.row_number}: {e}")

        Implementation Notes:
            - Use context managers for file/connection handling
            - Validate data before creating Transaction objects
            - Log warnings for skipped rows (if applicable)
            - Consider memory efficiency for large datasets
            - Preserve original transaction order
        """
        pass

    @abstractmethod
    def validate_source(self, source: str) -> bool:
        """
        Check if source is accessible and readable without loading data.

        This method allows pre-flight validation before attempting to load
        large datasets.

        Args:
            source: Path or identifier for the data source

        Returns:
            True if source exists and is readable, False otherwise

        Raises:
            No exceptions - returns False for any access issues

        Example:
            >>> loader = CSVTransactionLoader()
            >>> if loader.validate_source('expenses.csv'):
            ...     transactions = loader.load('expenses.csv')
            ... else:
            ...     print("File not accessible")

        Implementation Notes:
            - Check file existence (for file-based loaders)
            - Check read permissions
            - Check file is not empty (optional)
            - Do NOT load actual data (performance)
        """
        pass


class CSVTransactionLoader(TransactionLoader):
    """
    Loads transactions from CSV files.

    Expected CSV format:
        date,amount,category,description
        2025-01-15,42.50,Food,Lunch at cafe
        2025-01-16,120.00,Transportation,Monthly metro pass

    CSV Requirements:
        - First row must be header (will be skipped)
        - Exactly 4 columns: date, amount, category, description
        - Date format: YYYY-MM-DD (ISO 8601)
        - Amount: Positive decimal number
        - No empty fields

    Example:
        >>> loader = CSVTransactionLoader()
        >>> transactions = loader.load('expenses.csv')
        >>> print(f"Loaded {len(transactions)} transactions")
        Loaded 150 transactions

    Raises:
        DataLoadError: If file cannot be accessed or is empty
        ValidationError: If CSV format or data is invalid
    """

    REQUIRED_COLUMNS = {'date', 'amount', 'category', 'description'}

    def load(self, source: str) -> List[Transaction]:
        """
        Load transactions from CSV file.

        Validates CSV structure and data, then creates Transaction objects.
        Fails fast on first validation error.

        Args:
            source: Path to CSV file (absolute or relative)

        Returns:
            List of validated Transaction objects in file order.
            Returns empty list if file contains only headers.

        Raises:
            DataLoadError: If file not found, cannot be read, or is empty
            ValidationError: If CSV structure invalid or data fails validation

        See base class for additional details.
        """
        file_path = Path(source)

        # Check file existence
        if not file_path.exists():
            raise DataLoadError(f"File not found: {source}")

        # Check file readability
        if not file_path.is_file():
            raise DataLoadError(f"Path is not a file: {source}")

        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
                # Check if file is empty
                first_char = csvfile.read(1)
                if not first_char:
                    raise DataLoadError(f"File is empty: {source}")
                csvfile.seek(0)

                reader = csv.DictReader(csvfile)

                # Validate CSV has required columns
                if reader.fieldnames is None:
                    raise ValidationError("CSV file has no header row")

                actual_columns = set(reader.fieldnames)
                missing_columns = self.REQUIRED_COLUMNS - actual_columns
                if missing_columns:
                    missing_str = ', '.join(sorted(missing_columns))
                    raise ValidationError(
                        f"CSV missing required columns: {missing_str}"
                    )

                # Load and validate transactions
                transactions = []
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                    transaction = self._validate_and_create_transaction(row, row_num)
                    transactions.append(transaction)

                return transactions

        except ValidationError:
            raise
        except DataLoadError:
            raise
        except PermissionError as e:
            raise DataLoadError(f"Permission denied reading file: {source}") from e
        except UnicodeDecodeError as e:
            raise DataLoadError(f"File encoding error: {source}") from e
        except csv.Error as e:
            raise DataLoadError(f"CSV parsing error in {source}: {e}") from e
        except OSError as e:
            raise DataLoadError(f"Error reading file {source}: {e}") from e

    def validate_source(self, source: str) -> bool:
        """
        Check if CSV file is accessible and readable.

        Does not validate CSV content or structure - only checks file access.

        Args:
            source: Path to CSV file

        Returns:
            True if file exists and is readable, False otherwise

        See base class for additional details.
        """
        try:
            file_path = Path(source)
            if not file_path.exists() or not file_path.is_file():
                return False

            # Try to open file to check read permissions
            with open(file_path, 'r', encoding='utf-8'):
                pass
            return True
        except Exception:
            return False

    def _validate_and_create_transaction(
        self, row: dict, row_number: int
    ) -> Transaction:
        """
        Validate CSV row data and create Transaction object.

        Args:
            row: Dictionary from csv.DictReader with column names as keys
            row_number: Row number in CSV file (for error messages)

        Returns:
            Validated Transaction object

        Raises:
            ValidationError: If any field is invalid
        """
        # Extract and strip whitespace from all fields
        date_str = row.get('date', '').strip()
        amount_str = row.get('amount', '').strip()
        category = row.get('category', '').strip()
        description = row.get('description', '').strip()

        # Validate required fields are not empty
        if not date_str:
            raise ValidationError("Date field is empty", row_number=row_number)
        if not amount_str:
            raise ValidationError("Amount field is empty", row_number=row_number)
        if not category:
            raise ValidationError("Category field is empty", row_number=row_number)
        if not description:
            raise ValidationError("Description field is empty", row_number=row_number)

        # Validate and parse date
        try:
            transaction_date = date.fromisoformat(date_str)
        except ValueError as e:
            raise ValidationError(
                f"Invalid date format '{date_str}' (expected YYYY-MM-DD)",
                row_number=row_number
            ) from e

        # Validate and parse amount
        try:
            amount = Decimal(amount_str)
        except (InvalidOperation, ValueError) as e:
            raise ValidationError(
                f"Invalid amount '{amount_str}' (must be a number)",
                row_number=row_number
            ) from e

        # Validate amount is positive
        if amount <= 0:
            raise ValidationError(
                f"Amount must be positive, got {amount}",
                row_number=row_number
            )

        # Create Transaction object (will perform additional validation in __post_init__)
        try:
            return Transaction(
                date=transaction_date,
                amount=amount,
                category=category,
                description=description
            )
        except ValueError as e:
            raise ValidationError(str(e), row_number=row_number) from e
