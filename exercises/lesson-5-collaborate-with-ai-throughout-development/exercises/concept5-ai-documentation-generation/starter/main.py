#!/usr/bin/env python3
"""
Main entry point for expense tracker CLI application.

Usage:
    python main.py expenses.csv
    python main.py expenses.csv --report monthly
    python main.py expenses.csv --report top --top-n 20
"""

from expense_tracker.cli import main

if __name__ == '__main__':
    main()
