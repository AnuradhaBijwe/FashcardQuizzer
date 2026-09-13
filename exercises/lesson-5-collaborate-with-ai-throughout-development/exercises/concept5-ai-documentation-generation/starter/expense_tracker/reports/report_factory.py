"""
Factory for creating report mode instances.

This module implements the Factory pattern to encapsulate report strategy
creation and provide a registry for available report types.
"""

from typing import Dict, Type

from expense_tracker.reports.report_mode import (
    ReportMode,
    CategorySummaryReport,
    MonthlyTotalsReport,
    TopExpensesReport,
)
from expense_tracker.domain.exceptions import InvalidReportTypeError


class ReportFactory:
    """
    Factory for creating ReportMode instances.

    Provides centralized registration and creation of report strategies,
    making it easy to add new report types without modifying existing code.

    Usage:
        >>> factory = ReportFactory()
        >>> report = factory.create_report('category')
        >>> print(type(report))
        <class 'CategorySummaryReport'>

        >>> # Get available report types
        >>> print(factory.get_available_types())
        ['category', 'monthly', 'top']

        >>> # Handle invalid type
        >>> try:
        ...     factory.create_report('invalid')
        ... except InvalidReportTypeError as e:
        ...     print(f"Error: {e}")
    """

    # Registry mapping report type names to strategy classes
    _registry: Dict[str, Type[ReportMode]] = {
        'category': CategorySummaryReport,
        'monthly': MonthlyTotalsReport,
        'top': TopExpensesReport,
    }

    @classmethod
    def create_report(cls, report_type: str, **kwargs) -> ReportMode:
        """
        Create a report strategy instance.

        Args:
            report_type: Name of the report type (e.g., 'category', 'monthly')
            **kwargs: Additional arguments passed to strategy constructor
                     (e.g., top_n=20 for TopExpensesReport)

        Returns:
            Instantiated ReportMode strategy

        Raises:
            InvalidReportTypeError: When report_type is not registered

        Example:
            >>> factory = ReportFactory()
            >>> report = factory.create_report('top', top_n=20)
            >>> print(report.get_report_name())
            Top 20 Expenses
        """
        if report_type not in cls._registry:
            raise InvalidReportTypeError(
                report_type=report_type,
                available_types=cls.get_available_types()
            )

        strategy_class = cls._registry[report_type]
        return strategy_class(**kwargs)

    @classmethod
    def get_available_types(cls) -> list[str]:
        """
        Get list of registered report type names.

        Returns:
            Sorted list of available report type identifiers

        Example:
            >>> ReportFactory.get_available_types()
            ['category', 'monthly', 'top']
        """
        return sorted(cls._registry.keys())

    @classmethod
    def register_report(cls, name: str, strategy_class: Type[ReportMode]) -> None:
        """
        Register a new report strategy (for extensions).

        This method allows adding custom report types without modifying
        the factory source code.

        Args:
            name: Unique identifier for the report type
            strategy_class: ReportMode subclass to register

        Raises:
            ValueError: If name already registered
            TypeError: If strategy_class is not a ReportMode subclass

        Example:
            >>> class CustomReport(ReportMode):
            ...     # Implementation here
            ...     pass
            >>> ReportFactory.register_report('custom', CustomReport)
            >>> report = ReportFactory.create_report('custom')
        """
        if name in cls._registry:
            raise ValueError(f"Report type '{name}' already registered")

        if not issubclass(strategy_class, ReportMode):
            raise TypeError(f"{strategy_class} must be a ReportMode subclass")

        cls._registry[name] = strategy_class
