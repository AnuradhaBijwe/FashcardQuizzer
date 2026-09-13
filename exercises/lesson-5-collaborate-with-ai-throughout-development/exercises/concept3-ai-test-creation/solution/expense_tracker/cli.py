"""
Command-line interface orchestrator.

This module provides the main entry point for the expense tracker CLI,
coordinating all components to generate reports from expense data.
"""

import argparse
import sys
from pathlib import Path
from typing import NoReturn

from expense_tracker.data.transaction_loader import CSVTransactionLoader
from expense_tracker.reports.report_factory import ReportFactory
from expense_tracker.domain.exceptions import (
    ExpenseTrackerError,
    DataLoadError,
    ValidationError,
    InvalidReportTypeError,
    EmptyDatasetError,
)


class ExpenseTrackerCLI:
    """
    Command-line interface orchestrator for expense tracker.

    Responsibilities:
        - Parse command-line arguments
        - Coordinate data loading, processing, and display
        - Handle errors gracefully with user-friendly messages
        - Exit with appropriate status codes

    Usage:
        >>> cli = ExpenseTrackerCLI()
        >>> cli.run(['expenses.csv', '--report', 'category'])

    Design:
        - Follows Dependency Injection (dependencies passed to methods)
        - Depends on abstractions (TransactionLoader, ReportMode)
        - Handles all errors in one place (run method)
    """

    def __init__(self):
        """Initialize CLI with argument parser."""
        self.parser = self._create_argument_parser()

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure argument parser.

        Returns:
            Configured ArgumentParser instance

        Implementation notes:
            - Add positional argument for file path
            - Add --report flag for report type (default: 'category')
            - Add --top-n flag for TopExpensesReport (default: 10)
            - Add --help with clear usage examples
        """
        parser = argparse.ArgumentParser(
            description='Generate expense reports from CSV transaction data',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s expenses.csv
  %(prog)s expenses.csv --report monthly
  %(prog)s expenses.csv --report top --top-n 20

Available report types:
  category - Summary by expense category
  monthly  - Totals by month
  top      - Largest individual expenses
            """
        )

        parser.add_argument(
            'file',
            type=str,
            help='Path to CSV file containing expense data'
        )

        parser.add_argument(
            '--report',
            type=str,
            default='category',
            choices=['category', 'monthly', 'top'],
            help='Type of report to generate (default: category)'
        )

        parser.add_argument(
            '--top-n',
            type=int,
            default=10,
            metavar='N',
            help='Number of top expenses to show (for "top" report, default: 10)'
        )

        return parser

    def run(self, args: list[str] | None = None) -> int:
        """
        Main entry point for CLI execution.

        Args:
            args: Command-line arguments (uses sys.argv if None)

        Returns:
            Exit status code:
                0 - Success
                1 - Data loading error (file not found, invalid data)
                2 - Invalid arguments (unknown report type, bad flags)
                3 - Processing error (empty dataset, calculation error)

        Implementation workflow:
            1. Parse arguments
            2. Create loader and validate file
            3. Load transactions
            4. Create report strategy
            5. Generate and display report
            6. Handle errors with appropriate messages

        Example:
            >>> cli = ExpenseTrackerCLI()
            >>> exit_code = cli.run(['expenses.csv', '--report', 'monthly'])
            >>> sys.exit(exit_code)

        Error handling:
            - Catch all ExpenseTrackerError subclasses
            - Print user-friendly error messages to stderr
            - Return appropriate exit codes
            - Log full stack trace for debugging (optional)
        """
        try:
            # Parse arguments
            parsed_args = self.parser.parse_args(args)

            # Validate file exists before loading
            file_path = Path(parsed_args.file)
            if not file_path.exists():
                raise DataLoadError(f"File not found: {file_path}")

            # Load transactions
            loader = CSVTransactionLoader()
            transactions = loader.load(str(file_path))

            # Check for empty dataset
            if not transactions:
                raise EmptyDatasetError(
                    f"No valid transactions found in {file_path}"
                )

            # Create report strategy
            report_kwargs = {}
            if parsed_args.report == 'top':
                report_kwargs['top_n'] = parsed_args.top_n

            report = ReportFactory.create_report(
                parsed_args.report,
                **report_kwargs
            )

            # Generate and display report
            output = report.process_transactions(transactions)
            print(output)

            return 0

        except DataLoadError as e:
            print(f"Error loading data: {e}", file=sys.stderr)
            return 1

        except ValidationError as e:
            print(f"Validation error: {e}", file=sys.stderr)
            return 1

        except InvalidReportTypeError as e:
            print(f"Invalid report type: {e}", file=sys.stderr)
            return 2

        except EmptyDatasetError as e:
            print(f"No data to report: {e}", file=sys.stderr)
            return 3

        except ExpenseTrackerError as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 3

        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            return 130  # Standard exit code for SIGINT

        except Exception as e:
            # Catch-all for unexpected errors
            print(f"Unexpected error: {e}", file=sys.stderr)
            # In production, log full traceback here
            return 1


def main() -> NoReturn:
    """
    Main entry point for console script.

    This function is called when running:
        python -m expense_tracker
        or
        expense-tracker (if installed)

    Example:
        >>> if __name__ == '__main__':
        ...     main()
    """
    cli = ExpenseTrackerCLI()
    sys.exit(cli.run())
