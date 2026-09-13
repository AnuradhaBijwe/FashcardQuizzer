# Expense Tracker Implementation Guide

This guide provides detailed implementation notes for each interface in the expense tracker application.

## Table of Contents

1. [TransactionLoader Interface](#transactionloader-interface)
2. [ReportMode Interface](#reportmode-interface)
3. [Implementation Order](#implementation-order)
4. [Testing Strategy](#testing-strategy)
5. [Common Pitfalls](#common-pitfalls)

---

## TransactionLoader Interface

### Location
`expense_tracker/data/transaction_loader.py`

### Purpose
Abstract interface for loading transaction data from various sources (CSV, JSON, databases, APIs).

### Implementation Notes for CSVTransactionLoader

#### 1. `load(source: str) -> List[Transaction]`

**Requirements:**
- Read CSV file from the given path
- Parse each row into a Transaction object
- Validate data before creating Transaction objects
- Handle errors appropriately

**Implementation Steps:**

```python
def load(self, source: str) -> List[Transaction]:
    import csv
    from pathlib import Path

    # 1. Validate file exists
    path = Path(source)
    if not path.exists():
        raise DataLoadError(f"File not found: {source}")

    # 2. Check file is not empty
    if path.stat().st_size == 0:
        raise DataLoadError(f"File is empty: {source}")

    # 3. Read and parse CSV
    transactions = []
    try:
        with open(source, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # 4. Validate CSV has required columns
            expected_columns = {'date', 'amount', 'category', 'description'}
            if not expected_columns.issubset(set(reader.fieldnames or [])):
                raise ValidationError(
                    f"CSV missing required columns. "
                    f"Expected: {expected_columns}, "
                    f"Got: {set(reader.fieldnames or [])}"
                )

            # 5. Parse each row
            for row_num, row in enumerate(reader, start=2):  # start=2 (header is row 1)
                try:
                    # Parse date
                    transaction_date = date.fromisoformat(row['date'].strip())

                    # Parse amount
                    amount = Decimal(row['amount'].strip())

                    # Get category and description
                    category = row['category'].strip()
                    description = row['description'].strip()

                    # Create transaction (validates in __post_init__)
                    tx = Transaction(
                        date=transaction_date,
                        amount=amount,
                        category=category,
                        description=description
                    )
                    transactions.append(tx)

                except ValueError as e:
                    # Validation failed - include row number
                    raise ValidationError(str(e), row_number=row_num)
                except KeyError as e:
                    raise ValidationError(
                        f"Missing field: {e}",
                        row_number=row_num
                    )

    except FileNotFoundError:
        raise DataLoadError(f"File not found: {source}")
    except PermissionError:
        raise DataLoadError(f"Permission denied: {source}")

    return transactions
```

**Key Points:**
- Use `csv.DictReader` for robust CSV parsing
- Use `date.fromisoformat()` for ISO 8601 date parsing (YYYY-MM-DD)
- Use `Decimal` for monetary amounts (not float!)
- Include row numbers in validation errors (start=2 because row 1 is header)
- Let Transaction.__post_init__ handle business validation
- Use context manager (with statement) for file handling

#### 2. `validate_source(source: str) -> bool`

**Requirements:**
- Check if file exists and is readable
- Return boolean (no exceptions)
- Do not load actual data (performance)

**Implementation Steps:**

```python
def validate_source(self, source: str) -> bool:
    from pathlib import Path

    try:
        path = Path(source)

        # Check file exists
        if not path.exists():
            return False

        # Check it's a file (not directory)
        if not path.is_file():
            return False

        # Check we can read it
        if not path.stat().st_mode & 0o400:  # Read permission
            return False

        # Optional: Check file is not empty
        if path.stat().st_size == 0:
            return False

        return True

    except Exception:
        # Any error means source is not valid
        return False
```

**Key Points:**
- Never raise exceptions from this method
- Return False for any issues
- Check file existence, type, and permissions
- Don't actually open or read the file

---

## ReportMode Interface

### Location
`expense_tracker/reports/report_mode.py`

### Purpose
Strategy interface for different report types following Open/Closed Principle.

### Implementation Notes for CategorySummaryReport

#### 1. `process_transactions(transactions: List[Transaction]) -> str`

**Requirements:**
- Group transactions by category
- Calculate totals, counts, and averages
- Format as readable table
- Include grand total

**Implementation Steps:**

```python
def process_transactions(self, transactions: List[Transaction]) -> str:
    # 1. Validate non-empty
    if not transactions:
        raise EmptyDatasetError("No transactions to process")

    # 2. Aggregate by category
    from collections import defaultdict
    category_data = defaultdict(lambda: {'total': Decimal('0'), 'count': 0})

    for tx in transactions:
        category_data[tx.category]['total'] += tx.amount
        category_data[tx.category]['count'] += 1

    # 3. Calculate averages and prepare rows
    rows = []
    for category, data in category_data.items():
        avg = data['total'] / data['count']
        rows.append({
            'category': category,
            'total': data['total'],
            'count': data['count'],
            'average': avg
        })

    # 4. Sort by total (descending)
    rows.sort(key=lambda r: r['total'], reverse=True)

    # 5. Format output
    from expense_tracker.presentation.formatters import (
        format_header,
        format_currency,
        format_separator
    )

    output_lines = []
    output_lines.append(format_header("Category Summary Report"))
    output_lines.append("")

    # Header row
    output_lines.append(
        f"{'Category':<20} {'Total':>12} {'Count':>8} {'Average':>12}"
    )
    output_lines.append(format_separator(54, '-'))

    # Data rows
    grand_total = Decimal('0')
    total_count = 0

    for row in rows:
        output_lines.append(
            f"{row['category']:<20} "
            f"{format_currency(row['total']):>12} "
            f"{row['count']:>8} "
            f"{format_currency(row['average']):>12}"
        )
        grand_total += row['total']
        total_count += row['count']

    # Total row
    output_lines.append(format_separator(54, '-'))
    grand_avg = grand_total / total_count
    output_lines.append(
        f"{'TOTAL':<20} "
        f"{format_currency(grand_total):>12} "
        f"{total_count:>8} "
        f"{format_currency(grand_avg):>12}"
    )

    return '\n'.join(output_lines)
```

**Key Points:**
- Always validate non-empty dataset first
- Use `defaultdict` for easy aggregation
- Use `Decimal` for all calculations
- Sort logically (by total descending)
- Format consistently (alignment, decimal places)
- Include grand totals for context

#### 2. `get_report_name() -> str`

**Simple implementation:**

```python
def get_report_name(self) -> str:
    return "Category Summary"
```

### Implementation Notes for MonthlyTotalsReport

**Key differences from Category report:**
- Extract year-month from transaction dates
- Sort chronologically (not by amount)
- Format month as "YYYY-MM"

**Month extraction:**

```python
# In aggregation phase
month_key = tx.date.strftime('%Y-%m')  # e.g., "2025-01"
```

### Implementation Notes for TopExpensesReport

**Key differences:**
- Sort transactions by amount descending
- Take first N transactions
- Show individual transactions (not aggregated)
- Include date and description columns

**Implementation:**

```python
def process_transactions(self, transactions: List[Transaction]) -> str:
    if not transactions:
        raise EmptyDatasetError("No transactions to process")

    # Sort by amount descending and take top N
    sorted_txs = sorted(transactions, key=lambda t: t.amount, reverse=True)
    top_txs = sorted_txs[:self.top_n]

    # Format output with Date, Amount, Category, Description columns
    # ... (similar formatting pattern as Category report)
```

---

## Implementation Order

Recommended order for implementing the application:

### Phase 1: Domain Layer (Foundation)
1. ✅ `domain/models.py` - Already defined
2. ✅ `domain/exceptions.py` - Already defined
3. **Test**: `tests/test_models.py`

### Phase 2: Data Layer
4. **Implement**: `data/transaction_loader.py` (CSVTransactionLoader.load())
5. **Implement**: `data/transaction_loader.py` (CSVTransactionLoader.validate_source())
6. **Test**: `tests/test_csv_loader.py`

### Phase 3: Presentation Layer
7. **Implement**: `presentation/formatters.py` (all formatting utilities)
8. **Test**: Create `tests/test_formatters.py`

### Phase 4: Business Logic Layer
9. **Implement**: `reports/report_mode.py` (CategorySummaryReport)
10. **Test**: `tests/test_report_modes.py` (TestCategorySummaryReport)
11. **Implement**: `reports/report_mode.py` (MonthlyTotalsReport)
12. **Test**: `tests/test_report_modes.py` (TestMonthlyTotalsReport)
13. **Implement**: `reports/report_mode.py` (TopExpensesReport)
14. **Test**: `tests/test_report_modes.py` (TestTopExpensesReport)

### Phase 5: Factory
15. **Review**: `reports/report_factory.py` (already implemented)
16. **Test**: `tests/test_report_factory.py`

### Phase 6: CLI Integration
17. **Review**: `cli.py` (already implemented)
18. **Test**: `tests/test_cli.py` (integration tests)

### Phase 7: End-to-End Testing
19. **Manual test**: Run with `examples/sample_expenses.csv`
20. **Verify**: All report types work correctly

---

## Testing Strategy

### Unit Tests
- Test each class/function in isolation
- Use fixtures for test data
- Mock external dependencies (file system, etc.)

### Integration Tests
- Test CLI end-to-end
- Use real CSV fixtures
- Verify exit codes and output

### Test Fixtures Location
`tests/fixtures/`

**Required fixtures:**
- `valid_expenses.csv` - ✅ Already created
- `invalid_date.csv` - Create with invalid date format
- `invalid_format.csv` - Create with wrong number of columns
- `negative_amount.csv` - Create with negative amounts
- `empty.csv` - Create empty file

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_models

# Run with coverage
pip install coverage
coverage run -m unittest discover tests
coverage report
coverage html
```

---

## Common Pitfalls

### 1. Float vs Decimal for Money
❌ **Wrong:**
```python
amount = float(row['amount'])  # Rounding errors!
```

✅ **Correct:**
```python
amount = Decimal(row['amount'])  # Exact precision
```

### 2. Forgetting Row Numbers in Validation Errors
❌ **Wrong:**
```python
raise ValidationError("Invalid date")
```

✅ **Correct:**
```python
raise ValidationError("Invalid date", row_number=row_num)
```

### 3. Not Validating Empty Dataset
❌ **Wrong:**
```python
def process_transactions(self, transactions):
    # Directly process - will crash on empty list
    total = sum(tx.amount for tx in transactions)
```

✅ **Correct:**
```python
def process_transactions(self, transactions):
    if not transactions:
        raise EmptyDatasetError("No transactions to process")
    # Now safe to process
```

### 4. Hardcoding Column Widths
❌ **Wrong:**
```python
f"{category:20} {amount:10}"  # Too rigid
```

✅ **Better:**
```python
# Calculate max width dynamically or use constants
CATEGORY_WIDTH = 20
f"{category:<{CATEGORY_WIDTH}} {amount:>10}"
```

### 5. Not Closing File Handles
❌ **Wrong:**
```python
f = open(source, 'r')
# ... do stuff ...
# File might not close if error occurs
```

✅ **Correct:**
```python
with open(source, 'r') as f:
    # ... do stuff ...
    # File automatically closed
```

### 6. Catching Too Broad Exceptions
❌ **Wrong:**
```python
try:
    # ... load data ...
except Exception:
    raise DataLoadError("Something went wrong")  # Lost context!
```

✅ **Correct:**
```python
try:
    # ... load data ...
except FileNotFoundError:
    raise DataLoadError(f"File not found: {source}")
except PermissionError:
    raise DataLoadError(f"Permission denied: {source}")
# Let other exceptions propagate
```

---

## Next Steps

1. Implement TransactionLoader.load() method
2. Write tests for data loading
3. Implement presentation formatters
4. Implement report strategies one by one
5. Run end-to-end tests with sample data
6. Add additional report types as needed

## Questions?

- Check interface docstrings for detailed contracts
- Refer to SOLID principles in architecture design
- Run tests frequently during development
- Use type hints and let mypy catch errors early
