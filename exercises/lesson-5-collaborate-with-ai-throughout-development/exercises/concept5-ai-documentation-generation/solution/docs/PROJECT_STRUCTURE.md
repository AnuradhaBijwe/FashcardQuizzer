# Expense Tracker - Complete Project Structure

## Directory Tree

```
expense_tracker/
├── expense_tracker/              # Main application package
│   ├── __init__.py              # Package initialization
│   │
│   ├── domain/                  # Domain layer (core models)
│   │   ├── __init__.py
│   │   ├── models.py            # Transaction, ValidationResult data models
│   │   ├── exceptions.py        # Custom exception hierarchy
│   │   └── validators.py        # Data validation utilities (stub)
│   │
│   ├── data/                    # Data access layer
│   │   ├── __init__.py
│   │   └── transaction_loader.py # TransactionLoader ABC + CSVTransactionLoader
│   │
│   ├── reports/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── report_mode.py       # ReportMode ABC + concrete strategies
│   │   │                        #   - CategorySummaryReport
│   │   │                        #   - MonthlyTotalsReport
│   │   │                        #   - TopExpensesReport
│   │   └── report_factory.py    # ReportFactory for creating strategies
│   │
│   ├── presentation/            # Presentation layer
│   │   ├── __init__.py
│   │   └── formatters.py        # Terminal formatting utilities
│   │
│   └── cli.py                   # CLI orchestrator (main application logic)
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_models.py           # Unit tests for domain models
│   ├── test_csv_loader.py       # Unit tests for CSV loading
│   ├── test_report_modes.py     # Unit tests for report strategies
│   ├── test_report_factory.py   # Unit tests for factory
│   ├── test_cli.py              # Integration tests for CLI
│   │
│   └── fixtures/                # Test data
│       └── valid_expenses.csv   # Sample valid CSV for testing
│
├── examples/                    # Example data files
│   └── sample_expenses.csv      # Sample expense data for demonstration
│
├── docs/                        # Documentation
│   ├── IMPLEMENTATION_GUIDE.md  # Detailed implementation notes
│   ├── PROJECT_STRUCTURE.md     # This file
│   └── PROJECT_README.md        # Project overview and usage
│
├── main.py                      # Application entry point
└── README.md                    # Lesson instructions (not project docs)
```

## Module Descriptions

### Domain Layer (`expense_tracker/domain/`)

**Purpose**: Contains core business domain models and rules

#### `models.py` (Implemented)
- **Transaction**: Immutable dataclass representing a financial transaction
  - Fields: date, amount, category, description
  - Validation: Positive amounts, non-empty fields
- **ValidationResult**: Result of validation operations
  - Factory methods: `success()`, `failure()`

**Size**: ~100 lines
**Dependencies**: `datetime`, `decimal`, `dataclasses`
**Tests**: `tests/test_models.py`

#### `exceptions.py` (Implemented)
- **ExpenseTrackerError**: Base exception
- **DataLoadError**: File access issues
- **ValidationError**: Data validation failures (includes row context)
- **InvalidReportTypeError**: Unknown report type requested
- **EmptyDatasetError**: No data to process

**Size**: ~80 lines
**Dependencies**: None (stdlib only)
**Tests**: Covered in integration tests

#### `validators.py` (Stub - To Be Implemented)
- Utility functions for data validation
- Date format validation
- Amount validation
- Category/description validation

**Size**: ~80 lines (estimated)
**Dependencies**: `datetime`, `decimal`
**Tests**: To be added

---

### Data Layer (`expense_tracker/data/`)

**Purpose**: Handles data loading and storage access

#### `transaction_loader.py` (Interfaces Defined)
- **TransactionLoader (ABC)**: Abstract interface for loading transactions
  - Method: `load(source: str) -> List[Transaction]`
  - Method: `validate_source(source: str) -> bool`

- **CSVTransactionLoader**: CSV file implementation (to be implemented)
  - Reads CSV files
  - Validates format and data
  - Creates Transaction objects
  - Raises DataLoadError or ValidationError

**Size**: ~140 lines (with implementation)
**Dependencies**: `csv`, `pathlib`, `abc`
**Tests**: `tests/test_csv_loader.py`

**CSV Format Expected**:
```csv
date,amount,category,description
2025-01-15,42.50,Food,Lunch at cafe
```

---

### Reports Layer (`expense_tracker/reports/`)

**Purpose**: Business logic for report generation

#### `report_mode.py` (Interfaces Defined)
- **ReportMode (ABC)**: Strategy interface for report types
  - Method: `process_transactions(transactions: List[Transaction]) -> str`
  - Method: `get_report_name() -> str`

- **CategorySummaryReport**: Groups by category (to be implemented)
- **MonthlyTotalsReport**: Groups by month (to be implemented)
- **TopExpensesReport**: Shows top N expenses (to be implemented)

**Size**: ~200 lines total
**Dependencies**: `abc`, `typing`, `domain.models`
**Tests**: `tests/test_report_modes.py`

#### `report_factory.py` (Implemented)
- **ReportFactory**: Factory for creating report strategies
  - Method: `create_report(report_type: str, **kwargs) -> ReportMode`
  - Method: `get_available_types() -> list[str]`
  - Method: `register_report(name: str, strategy_class: Type[ReportMode])`

**Size**: ~100 lines
**Dependencies**: `report_mode`, `domain.exceptions`
**Tests**: `tests/test_report_factory.py`

**Registry**:
```python
{
    'category': CategorySummaryReport,
    'monthly': MonthlyTotalsReport,
    'top': TopExpensesReport,
}
```

---

### Presentation Layer (`expense_tracker/presentation/`)

**Purpose**: Formatting for terminal display

#### `formatters.py` (Stubs Defined)
- `format_currency(amount: Decimal, symbol: str) -> str`
- `format_table(rows: List[Dict], headers: List[str], ...) -> str`
- `format_separator(width: int, char: str) -> str`
- `format_header(title: str, width: int, underline_char: str) -> str`
- `format_summary_line(label: str, value: str, width: int) -> str`
- `truncate_text(text: str, max_length: int, suffix: str) -> str`

**Size**: ~150 lines (with implementation)
**Dependencies**: `decimal`, `typing`
**Tests**: To be added (`tests/test_formatters.py`)

---

### CLI Layer

#### `cli.py` (Implemented)
- **ExpenseTrackerCLI**: Main orchestrator
  - Parses command-line arguments
  - Coordinates all components
  - Handles errors
  - Returns exit codes

**Size**: ~150 lines
**Dependencies**: `argparse`, `sys`, `pathlib`
**Tests**: `tests/test_cli.py`

**Arguments**:
- `file`: CSV file path (positional)
- `--report`: Report type (category, monthly, top)
- `--top-n`: Number for top expenses report

**Exit Codes**:
- 0: Success
- 1: Data loading error
- 2: Invalid arguments
- 3: Processing error

#### `main.py` (Implemented)
Entry point script that calls `cli.main()`

**Size**: ~10 lines
**Dependencies**: `cli`
**Usage**: `python main.py expenses.csv --report category`

---

## Test Structure

### Unit Tests

#### `tests/test_models.py`
Tests for Transaction and ValidationResult models:
- Valid transaction creation
- Validation errors (negative amounts, empty fields)
- Immutability
- ValidationResult factory methods

#### `tests/test_csv_loader.py`
Tests for CSVTransactionLoader:
- Loading valid CSV files
- File not found errors
- Invalid CSV format
- Invalid data (dates, amounts)
- Empty files
- Source validation

#### `tests/test_report_modes.py`
Tests for report strategies:
- CategorySummaryReport: grouping, totals, formatting
- MonthlyTotalsReport: month grouping, chronological order
- TopExpensesReport: sorting, limiting, top_n validation
- Empty dataset handling

#### `tests/test_report_factory.py`
Tests for ReportFactory:
- Creating registered report types
- Invalid report type errors
- Custom report registration
- Available types listing

#### `tests/test_cli.py`
Integration tests for CLI:
- Successful execution
- Error handling
- Argument parsing
- Exit codes
- Output routing (stdout/stderr)

### Test Fixtures

#### `tests/fixtures/valid_expenses.csv`
Sample valid CSV data for testing (6 transactions)

**Additional fixtures needed** (to be created):
- `invalid_date.csv` - Invalid date format
- `invalid_format.csv` - Wrong column structure
- `negative_amount.csv` - Negative amounts
- `empty.csv` - Empty file

---

## Examples

### `examples/sample_expenses.csv`
Realistic sample data (20 transactions) for demonstration:
- Multiple categories
- Two months of data
- Various amounts
- Realistic descriptions

**Usage**: `python main.py examples/sample_expenses.csv`

---

## Documentation

### `docs/IMPLEMENTATION_GUIDE.md`
Comprehensive implementation guide with:
- Step-by-step implementation notes
- Code examples
- Common pitfalls
- Testing strategy
- Implementation order

### `docs/PROJECT_STRUCTURE.md` (This file)
Complete project structure reference

### `docs/PROJECT_README.md`
Project overview and user documentation

---

## Dependencies

### Runtime Dependencies
**None** - Uses Python standard library only:
- `abc` - Abstract base classes
- `argparse` - CLI argument parsing
- `csv` - CSV file reading
- `dataclasses` - Data model definitions
- `datetime` - Date handling
- `decimal` - Precise monetary calculations
- `pathlib` - Path manipulation
- `sys` - System operations
- `typing` - Type hints

### Development Dependencies
(Optional, not in stdlib):
- `pytest` - Testing framework
- `mypy` - Static type checking
- `black` - Code formatting
- `coverage` - Test coverage

**Install dev dependencies**:
```bash
pip install pytest mypy black coverage
```

---

## File Size Summary

| File | Lines | Status |
|------|-------|--------|
| `domain/models.py` | ~100 | ✅ Implemented |
| `domain/exceptions.py` | ~80 | ✅ Implemented |
| `domain/validators.py` | ~80 | ⏳ Stub |
| `data/transaction_loader.py` | ~140 | ⏳ Interfaces only |
| `reports/report_mode.py` | ~200 | ⏳ Interfaces only |
| `reports/report_factory.py` | ~100 | ✅ Implemented |
| `presentation/formatters.py` | ~150 | ⏳ Stubs only |
| `cli.py` | ~150 | ✅ Implemented |
| `main.py` | ~10 | ✅ Implemented |
| **Total** | **~1,010** | **30% complete** |

---

## Import Path Strategy

### Internal Imports

```python
# From domain layer
from expense_tracker.domain.models import Transaction, ValidationResult
from expense_tracker.domain.exceptions import DataLoadError, ValidationError

# From data layer
from expense_tracker.data.transaction_loader import TransactionLoader, CSVTransactionLoader

# From reports layer
from expense_tracker.reports.report_mode import ReportMode
from expense_tracker.reports.report_factory import ReportFactory

# From presentation layer
from expense_tracker.presentation.formatters import format_currency, format_table
```

### External Usage

```python
# Run as module
python -m expense_tracker.cli

# Or via entry point
python main.py expenses.csv
```

---

## Next Steps

### To Complete Implementation

1. **Implement CSVTransactionLoader** (`data/transaction_loader.py`)
2. **Implement formatters** (`presentation/formatters.py`)
3. **Implement CategorySummaryReport** (`reports/report_mode.py`)
4. **Implement MonthlyTotalsReport** (`reports/report_mode.py`)
5. **Implement TopExpensesReport** (`reports/report_mode.py`)
6. **Write all unit tests**
7. **Create additional test fixtures**
8. **Run end-to-end tests**

See `docs/IMPLEMENTATION_GUIDE.md` for detailed implementation notes.
