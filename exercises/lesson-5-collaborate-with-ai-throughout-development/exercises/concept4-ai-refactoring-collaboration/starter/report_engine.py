"""
ReportEngine - Orchestrates report generation using pluggable strategies.

This module implements the Facade pattern to coordinate transaction loading
and report processing. It provides a simple interface that hides the complexity
of working with multiple components (loaders and report strategies).
"""

from typing import Dict, Any


class ReportEngine:
    """Orchestrates report generation using pluggable strategies."""

    def __init__(self, loader):
        """
        Initialize with a transaction loader.

        Args:
            loader: TransactionLoader instance for loading transaction data
        """
        self.loader = loader

    def generate_report(self, filepath: str, mode) -> Dict[str, Any]:
        """
        Generate report from file using specified mode.

        Workflow:
        1. Load transactions from file using loader
        2. Process transactions using mode strategy
        3. Return formatted report data

        Args:
            filepath: Path to the transaction data file
            mode: ReportMode strategy for processing transactions

        Returns:
            Dictionary containing report data from the mode's processing

        Raises:
            FileNotFoundError: If file doesn't exist (propagated from loader)
            ValueError: If data is invalid (propagated from loader or mode)
        """
        transactions = self.loader.load(filepath)
        report_data = mode.process_transactions(transactions)
        return report_data
