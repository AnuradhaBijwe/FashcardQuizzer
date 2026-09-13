"""
Abstract interface for report generation strategies.

This module implements the Strategy pattern for different report types,
following the Open/Closed Principle for easy extensibility.

The Strategy pattern allows swapping report algorithms at runtime without
modifying client code. Each strategy encapsulates a specific way to analyze
and present transaction data.

Example Usage:
    >>> from expense_tracker.reports.report_mode import CategorySummaryReport
    >>> from expense_tracker.domain.models import Transaction
    >>> from datetime import date
    >>> from decimal import Decimal
    >>>
    >>> transactions = [
    ...     Transaction(date(2025, 1, 15), Decimal('42.50'), 'Food', 'Lunch'),
    ...     Transaction(date(2025, 1, 16), Decimal('120.00'), 'Transport', 'Metro pass'),
    ... ]
    >>>
    >>> report = CategorySummaryReport()
    >>> output = report.process_transactions(transactions)
    >>> print(output)
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List

from expense_tracker.domain.models import Transaction
from expense_tracker.domain.exceptions import EmptyDatasetError


class ReportMode(ABC):
    """
    Abstract base class for report generation strategies.

    This interface defines the contract for processing transactions and
    generating formatted reports. Each concrete implementation represents
    a different way to analyze and present expense data.

    The Strategy pattern allows:
        - Adding new report types without modifying existing code
        - Swapping report strategies at runtime
        - Independent testing of each report type
        - Reusable report logic across different interfaces (CLI, Web, etc.)

    Implementations must:
        1. Process transaction list
        2. Perform necessary aggregations/calculations
        3. Format results for display
        4. Return formatted string ready for terminal output

    Example implementations:
        - CategorySummaryReport: Group by category, show totals
        - MonthlyTotalsReport: Group by month, show trends
        - TopExpensesReport: Show largest N transactions
    """

    @abstractmethod
    def process_transactions(self, transactions: List[Transaction]) -> str:
        """
        Process transactions and generate formatted report.

        This method is the core of the Strategy pattern. Each implementation
        defines its own logic for analyzing transactions and formatting output.

        Processing typically involves:
            1. Validation (non-empty dataset)
            2. Aggregation (grouping, summing, sorting)
            3. Calculation (totals, averages, percentages)
            4. Formatting (tables, charts, summaries)

        Args:
            transactions: List of Transaction objects to analyze.
                         Must be non-empty.
                         Transactions may be pre-filtered by caller
                         (e.g., by date range or category).

        Returns:
            Formatted report as multi-line string ready for terminal display.

            Format requirements:
                - Human-readable plain text
                - Properly aligned columns (if tabular)
                - Clear section headers
                - Total/summary at end
                - Fits in standard terminal width (80-120 chars)

        Raises:
            EmptyDatasetError: When transactions list is empty.
                Raised before any processing to fail fast.

            ValueError: When transactions contain invalid data that prevents
                report generation (e.g., all amounts are zero).

        Example:
            >>> report = CategorySummaryReport()
            >>> transactions = [
            ...     Transaction(date(2025,1,15), Decimal('42.50'), 'Food', 'Lunch'),
            ...     Transaction(date(2025,1,16), Decimal('120.00'), 'Transport', 'Metro'),
            ...     Transaction(date(2025,1,17), Decimal('35.00'), 'Food', 'Groceries'),
            ... ]
            >>> output = report.process_transactions(transactions)
            >>> print(output)
            Category Summary Report
            =======================
            Category        Total      Count   Avg
            Food          $ 77.50          2   $ 38.75
            Transport     $120.00          1   $120.00
            -----------------------------------------
            TOTAL         $197.50          3   $ 65.83

            >>> # Empty dataset handling
            >>> try:
            ...     report.process_transactions([])
            ... except EmptyDatasetError:
            ...     print("No transactions to report")

        Implementation Notes:
            - Validate transactions list is not empty (raise EmptyDatasetError)
            - Use Decimal for all monetary calculations (avoid float rounding)
            - Sort output logically (by amount descending, alphabetically, etc.)
            - Include totals/summaries for context
            - Use consistent formatting (alignment, decimal places)
            - Consider terminal width constraints
            - Add visual separators (lines, spacing) for readability
        """
        pass

    @abstractmethod
    def get_report_name(self) -> str:
        """
        Return human-readable name for this report type.

        Used for:
            - CLI help text
            - Report headers
            - Logging and error messages

        Returns:
            Short descriptive name (e.g., "Category Summary", "Monthly Totals")

        Example:
            >>> report = CategorySummaryReport()
            >>> print(report.get_report_name())
            Category Summary
        """
        pass


class CategorySummaryReport(ReportMode):
    """
    Groups transactions by category and shows totals.

    This strategy aggregates all transactions by their category field,
    calculating total spending, transaction count, and average per category.
    Results are sorted by total amount to highlight biggest spending areas.

    Use cases:
        - Identify which expense categories consume most budget
        - Compare spending across different categories
        - Budget planning and allocation

    Output format:
        - One row per category
        - Columns: Category name, Total amount, Count, Average
        - Sorted by total amount (descending)
        - Grand total at bottom

    Example output:
        Category Summary Report
        =======================
        Category        Total      Count   Avg
        Food          $ 450.75         12   $ 37.56
        Transport     $ 320.00          8   $ 40.00
        Utilities     $ 215.50          3   $ 71.83
        -----------------------------------------
        TOTAL         $ 986.25         23   $ 42.88
    """

    def process_transactions(self, transactions: List[Transaction]) -> str:
        """
        Generate category summary report with aggregated totals.

        Groups transactions by category, sums amounts, and formats output
        as a table sorted by total spending (highest to lowest).

        Args:
            transactions: List of Transaction objects to analyze

        Returns:
            Formatted report string with category totals and statistics

        Raises:
            EmptyDatasetError: If transactions list is empty

        Example:
            >>> from datetime import date
            >>> from decimal import Decimal
            >>> txns = [
            ...     Transaction(date(2025, 1, 15), Decimal('42.50'), 'Food', 'Lunch'),
            ...     Transaction(date(2025, 1, 16), Decimal('35.00'), 'Food', 'Dinner'),
            ... ]
            >>> report = CategorySummaryReport()
            >>> print(report.process_transactions(txns))
        """
        # Validate non-empty dataset
        if not transactions:
            raise EmptyDatasetError("Cannot generate report from empty transaction list")

        # Group transactions by category
        category_data = defaultdict(list)
        for transaction in transactions:
            category_data[transaction.category].append(transaction.amount)

        # Calculate totals, counts, and averages for each category
        category_stats = {}
        for category, amounts in category_data.items():
            total = sum(amounts)
            count = len(amounts)
            average = total / count
            category_stats[category] = {
                'total': total,
                'count': count,
                'average': average
            }

        # Sort categories by total amount (descending)
        sorted_categories = sorted(
            category_stats.items(),
            key=lambda item: item[1]['total'],
            reverse=True
        )

        # Calculate grand totals
        grand_total = sum(stats['total'] for stats in category_stats.values())
        grand_count = sum(stats['count'] for stats in category_stats.values())
        grand_average = grand_total / grand_count if grand_count > 0 else 0

        # Format output
        lines = []
        lines.append("Category Summary Report")
        lines.append("=" * 50)
        lines.append(f"{'Category':<20} {'Total':>12} {'Count':>8} {'Avg':>10}")
        lines.append("-" * 50)

        for category, stats in sorted_categories:
            lines.append(
                f"{category:<20} "
                f"${stats['total']:>11,.2f} "
                f"{stats['count']:>8} "
                f"${stats['average']:>9,.2f}"
            )

        lines.append("-" * 50)
        lines.append(
            f"{'TOTAL':<20} "
            f"${grand_total:>11,.2f} "
            f"{grand_count:>8} "
            f"${grand_average:>9,.2f}"
        )

        return '\n'.join(lines)

    def get_report_name(self) -> str:
        """Return 'Category Summary'."""
        return "Category Summary"


class MonthlyTotalsReport(ReportMode):
    """
    Groups transactions by month and shows totals over time.

    This strategy aggregates transactions by month, allowing analysis of
    spending patterns over time. Useful for identifying seasonal trends,
    tracking monthly budgets, and comparing periods.

    Use cases:
        - Track monthly spending trends over time
        - Identify months with highest/lowest expenses
        - Budget vs. actual comparison by month
        - Seasonal spending analysis

    Output format:
        - One row per month
        - Columns: Month, Total amount, Count, Average
        - Sorted chronologically (oldest first)
        - Grand total at bottom

    Example output:
        Monthly Totals Report
        =====================
        Month           Total      Count   Avg
        2025-01       $1,234.56       45   $ 27.43
        2025-02       $1,089.23       38   $ 28.66
        2025-03       $1,456.78       52   $ 28.01
        -----------------------------------------
        TOTAL         $3,780.57      135   $ 28.00
    """

    def process_transactions(self, transactions: List[Transaction]) -> str:
        """
        Generate monthly totals report with time-based aggregation.

        Groups transactions by month (YYYY-MM format), sums amounts, and
        formats output chronologically to show spending trends over time.

        Args:
            transactions: List of Transaction objects to analyze

        Returns:
            Formatted report string with monthly totals and statistics

        Raises:
            EmptyDatasetError: If transactions list is empty

        Example:
            >>> from datetime import date
            >>> from decimal import Decimal
            >>> txns = [
            ...     Transaction(date(2025, 1, 15), Decimal('100.00'), 'Food', 'Lunch'),
            ...     Transaction(date(2025, 2, 10), Decimal('200.00'), 'Transport', 'Metro'),
            ... ]
            >>> report = MonthlyTotalsReport()
            >>> print(report.process_transactions(txns))
        """
        # Validate non-empty dataset
        if not transactions:
            raise EmptyDatasetError("Cannot generate report from empty transaction list")

        # Group transactions by month
        monthly_data = defaultdict(list)
        for transaction in transactions:
            # Extract year-month in YYYY-MM format
            month_key = transaction.date.strftime('%Y-%m')
            monthly_data[month_key].append(transaction.amount)

        # Calculate totals, counts, and averages for each month
        monthly_stats = {}
        for month, amounts in monthly_data.items():
            total = sum(amounts)
            count = len(amounts)
            average = total / count
            monthly_stats[month] = {
                'total': total,
                'count': count,
                'average': average
            }

        # Sort months chronologically
        sorted_months = sorted(monthly_stats.items(), key=lambda item: item[0])

        # Calculate grand totals
        grand_total = sum(stats['total'] for stats in monthly_stats.values())
        grand_count = sum(stats['count'] for stats in monthly_stats.values())
        grand_average = grand_total / grand_count if grand_count > 0 else 0

        # Format output
        lines = []
        lines.append("Monthly Totals Report")
        lines.append("=" * 50)
        lines.append(f"{'Month':<15} {'Total':>12} {'Count':>8} {'Avg':>10}")
        lines.append("-" * 50)

        for month, stats in sorted_months:
            lines.append(
                f"{month:<15} "
                f"${stats['total']:>11,.2f} "
                f"{stats['count']:>8} "
                f"${stats['average']:>9,.2f}"
            )

        lines.append("-" * 50)
        lines.append(
            f"{'TOTAL':<15} "
            f"${grand_total:>11,.2f} "
            f"{grand_count:>8} "
            f"${grand_average:>9,.2f}"
        )

        return '\n'.join(lines)

    def get_report_name(self) -> str:
        """Return 'Monthly Totals'."""
        return "Monthly Totals"


class TopExpensesReport(ReportMode):
    """
    Shows the N largest individual transactions.

    Output format:
        - Configurable number of top transactions (default: 10)
        - Columns: Date, Amount, Category, Description
        - Sorted by amount (descending)
        - Total of displayed transactions

    Example output:
        Top 10 Expenses Report
        ======================
        Date         Amount    Category        Description
        2025-01-15  $450.00   Electronics     New keyboard
        2025-01-22  $320.00   Transportation  Flight ticket
        2025-02-03  $215.50   Food            Restaurant dinner
        ...
        ---------------------------------------------------------
        TOTAL (top 10)  $1,892.75

    Implementation notes:
        - Sort transactions by amount descending
        - Take first N transactions
        - Truncate long descriptions (max 30 chars)
        - Include rank numbers (optional)
    """

    def __init__(self, top_n: int = 10):
        """
        Initialize report with configurable limit.

        Args:
            top_n: Number of top expenses to show (default: 10)

        Raises:
            ValueError: If top_n < 1
        """
        if top_n < 1:
            raise ValueError(f"top_n must be positive, got {top_n}")
        self.top_n = top_n

    def process_transactions(self, transactions: List[Transaction]) -> str:
        """
        Generate top expenses report showing largest transactions.

        Sorts transactions by amount descending and displays the top N
        with full details (date, amount, category, description).

        Args:
            transactions: List of Transaction objects to analyze

        Returns:
            Formatted report string with top N expenses

        Raises:
            EmptyDatasetError: If transactions list is empty

        Example:
            >>> from datetime import date
            >>> from decimal import Decimal
            >>> txns = [
            ...     Transaction(date(2025, 1, 15), Decimal('450.00'), 'Electronics', 'New keyboard'),
            ...     Transaction(date(2025, 1, 22), Decimal('320.00'), 'Transport', 'Flight ticket'),
            ... ]
            >>> report = TopExpensesReport(top_n=2)
            >>> print(report.process_transactions(txns))
        """
        # Validate non-empty dataset
        if not transactions:
            raise EmptyDatasetError("Cannot generate report from empty transaction list")

        # Sort transactions by amount (descending)
        sorted_transactions = sorted(
            transactions,
            key=lambda t: t.amount,
            reverse=True
        )

        # Take top N transactions (or all if fewer than N)
        top_transactions = sorted_transactions[:self.top_n]
        actual_count = len(top_transactions)

        # Calculate total of displayed transactions
        total_amount = sum(t.amount for t in top_transactions)

        # Format output
        lines = []
        lines.append(f"Top {self.top_n} Expenses Report")
        lines.append("=" * 80)
        lines.append(f"{'Date':<12} {'Amount':>12} {'Category':<20} {'Description':<30}")
        lines.append("-" * 80)

        for transaction in top_transactions:
            # Truncate long descriptions to fit in column
            description = transaction.description
            if len(description) > 30:
                description = description[:27] + "..."

            lines.append(
                f"{transaction.date} "
                f"${transaction.amount:>11,.2f} "
                f"{transaction.category:<20} "
                f"{description:<30}"
            )

        lines.append("-" * 80)
        lines.append(f"TOTAL (top {actual_count})  ${total_amount:>11,.2f}")

        # Add note if fewer transactions than requested
        if actual_count < self.top_n:
            lines.append("")
            lines.append(f"Note: Only {actual_count} transaction(s) available")

        return '\n'.join(lines)

    def get_report_name(self) -> str:
        """Return 'Top N Expenses' where N is the configured limit."""
        return f"Top {self.top_n} Expenses"
