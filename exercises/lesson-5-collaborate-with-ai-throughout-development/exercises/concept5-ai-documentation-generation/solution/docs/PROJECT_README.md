# Expense Tracker CLI

A command-line expense tracking and reporting tool built with Python following SOLID principles.

## Features

- 📊 Load transaction data from CSV files
- 📈 Generate multiple report types:
  - **Category Summary**: Group expenses by category with totals
  - **Monthly Totals**: Track spending trends over time
  - **Top Expenses**: Identify largest individual transactions
- 🔧 Extensible architecture for adding new report types
- ✅ Comprehensive error handling and validation
- 🧪 Fully testable with clean separation of concerns

## Quick Start

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses standard library only)

### Installation

```bash
# Clone or download the project
cd expense_tracker

# No installation required - uses Python standard library only
```

### Usage

```bash
# Basic usage - generates category summary report
python main.py expenses.csv

# Generate monthly totals report
python main.py expenses.csv --report monthly

# Show top 20 expenses
python main.py expenses.csv --report top --top-n 20

# Try with sample data
python main.py examples/sample_expenses.csv
```

### CSV File Format

Your CSV file must have the following format:

```csv
date,amount,category,description
2025-01-15,42.50,Food,Lunch at cafe
2025-01-16,120.00,Transportation,Monthly metro pass
2025-01-17,35.00,Food,Groceries
```

**Requirements:**
- Header row with columns: `date`, `amount`, `category`, `description`
- Date format: `YYYY-MM-DD` (ISO 8601)
- Amount: Positive decimal number
- All fields required (no empty values)

## Project Structure

See `docs/PROJECT_STRUCTURE.md` for detailed structure documentation.

## Architecture

This application follows **SOLID principles** and uses several design patterns.

### Design Patterns

1. **Strategy Pattern** - Different report types (CategorySummaryReport, MonthlyTotalsReport, TopExpensesReport)
2. **Factory Pattern** - ReportFactory creates report strategies
3. **Repository Pattern** - TransactionLoader abstracts data access
4. **Dependency Injection** - Components receive dependencies through constructors

### Data Flow

```
CSV File → TransactionLoader → List[Transaction] → ReportMode → Formatted String → Terminal
```

## Development

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test module
python -m unittest tests.test_models
```

### Adding a New Report Type

See `docs/IMPLEMENTATION_GUIDE.md` for detailed implementation notes.

## Documentation

- `docs/IMPLEMENTATION_GUIDE.md` - Detailed implementation notes for each interface
- `docs/PROJECT_STRUCTURE.md` - Complete project structure reference
- `docs/ARCHITECTURE.md` - Architecture decisions and design patterns

## License

This project is provided as-is for educational purposes.
