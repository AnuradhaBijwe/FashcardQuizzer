"""
Terminal output formatting utilities.

This module provides reusable formatting functions for displaying data
in the terminal with proper alignment, borders, and visual hierarchy.
"""

from decimal import Decimal
from typing import List, Dict, Any


def format_currency(amount: Decimal, symbol: str = '$') -> str:
    """
    Format decimal amount as currency string.

    Args:
        amount: Decimal value to format
        symbol: Currency symbol (default: '$')

    Returns:
        Formatted currency string with 2 decimal places

    Example:
        >>> format_currency(Decimal('1234.56'))
        '$1,234.56'
        >>> format_currency(Decimal('42.5'))
        '$42.50'
    """
    return f"{symbol}{amount:,.2f}"


def format_table(
    rows: List[Dict[str, Any]],
    headers: List[str],
    column_widths: Dict[str, int] | None = None,
    align: Dict[str, str] | None = None
) -> str:
    """
    Format data as aligned table with headers.

    Args:
        rows: List of dictionaries with column data
        headers: List of column header names (keys in row dicts)
        column_widths: Optional dict mapping header to width (auto-calculated if None)
        align: Optional dict mapping header to alignment ('left', 'right', 'center')
               Defaults to 'left' for text, 'right' for numbers

    Returns:
        Multi-line string containing formatted table

    Example:
        >>> rows = [
        ...     {'name': 'Food', 'amount': Decimal('42.50'), 'count': 5},
        ...     {'name': 'Transport', 'amount': Decimal('120.00'), 'count': 2},
        ... ]
        >>> headers = ['name', 'amount', 'count']
        >>> print(format_table(rows, headers))
        Name         Amount   Count
        --------------------------
        Food         $42.50       5
        Transport   $120.00       2

    Implementation notes:
        - Auto-detect column widths based on content
        - Right-align numeric columns by default
        - Add separator line after headers
        - Handle None/missing values gracefully
    """
    raise NotImplementedError("format_table() must be implemented")


def format_separator(width: int = 80, char: str = '-') -> str:
    """
    Create horizontal separator line.

    Args:
        width: Line width in characters (default: 80)
        char: Character to use for line (default: '-')

    Returns:
        Separator line string

    Example:
        >>> print(format_separator(40, '='))
        ========================================
    """
    return char * width


def format_header(title: str, width: int = 80, underline_char: str = '=') -> str:
    """
    Format report title with underline.

    Args:
        title: Report title text
        width: Total width (default: 80)
        underline_char: Character for underline (default: '=')

    Returns:
        Multi-line string with title and underline

    Example:
        >>> print(format_header("Category Summary"))
        Category Summary
        ================
    """
    lines = [title, underline_char * len(title)]
    return '\n'.join(lines)


def format_summary_line(label: str, value: str, width: int = 80) -> str:
    """
    Format summary line with right-aligned value.

    Args:
        label: Left-aligned label text
        value: Right-aligned value text
        width: Total line width (default: 80)

    Returns:
        Formatted line with label and value

    Example:
        >>> print(format_summary_line("TOTAL", "$1,234.56", width=40))
        TOTAL                          $1,234.56
    """
    padding = width - len(label) - len(value)
    return f"{label}{' ' * padding}{value}"


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate text to maximum length with ellipsis.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncated (default: '...')

    Returns:
        Truncated text with suffix if needed

    Example:
        >>> truncate_text("Very long description here", 15)
        'Very long de...'
        >>> truncate_text("Short", 15)
        'Short'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
