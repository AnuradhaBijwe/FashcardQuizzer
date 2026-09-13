# Expense Tracker CLI

A simple command-line tool for tracking and analyzing your personal expenses. Load your expense data from CSV files and generate insightful reports to understand your spending patterns across categories, months, and individual transactions.

## Overview

Expense Tracker CLI helps you visualize and analyze your spending habits without requiring any programming knowledge. Simply prepare your expense data in a CSV file, and the tool generates formatted reports showing:
- **Category summaries** - See how much you spend on Food, Transportation, Utilities, etc.
- **Monthly breakdowns** - Track your spending trends over time
- **Top expenses** - Identify your largest individual purchases

Perfect for personal budgeting, expense tracking, or understanding where your money goes each month.

---

## Installation

### Prerequisites

- **Python 3.8 or higher** (check with `python --version` or `python3 --version`)
- No external libraries needed - uses only Python standard library

### Setup Steps

1. **Clone or download this repository:**
   ```bash
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Verify the installation works:**
   ```bash
   python main.py examples/sample_expenses.csv
   ```

   You should see a formatted category summary report. If you see the report, you're all set!

---

## Quick Start

The simplest way to use the expense tracker is with the included sample data:

```bash
python main.py examples/sample_expenses.csv
```

**Expected output:**
```
Category Summary Report
==================================================
Category                    Total    Count        Avg
--------------------------------------------------
Shopping             $     575.00        2 $   287.50
Healthcare           $     500.00        2 $   250.00
Utilities            $     461.00        3 $   153.67
Food                 $     277.54        8 $    34.69
Transportation       $     265.00        3 $    88.33
Entertainment        $     164.99        2 $    82.50
--------------------------------------------------
TOTAL                $   2,243.53       20 $   112.18
```

---

## Usage

### Basic Command Structure

```bash
python main.py <csv-file> [options]
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `<csv-file>` | Path to your expense CSV file (required) | - |
| `--report <type>` | Type of report: `category`, `monthly`, or `top` | `category` |
| `--top-n <number>` | Number of top expenses to show (only for `top` report) | `10` |
| `--help` | Show help message with examples | - |

### CSV Format Requirements

Your CSV file must have these four columns in this exact order:

```csv
date,amount,category,description
```

**Column specifications:**
- `date` - Date in YYYY-MM-DD format (e.g., 2025-01-15)
- `amount` - Positive number with up to 2 decimal places (e.g., 42.50)
- `category` - Category name (e.g., Food, Transportation, Utilities)
- `description` - Brief description of the expense

**Example CSV file:**
```csv
date,amount,category,description
2025-01-05,52.30,Food,Weekly groceries
2025-01-08,12.50,Food,Coffee shop
2025-01-10,85.00,Transportation,Gas
2025-01-12,150.00,Utilities,Internet bill
2025-01-15,42.50,Food,Lunch at cafe
```

### Report Types

#### 1. Category Report (default)

Groups expenses by category and shows totals, counts, and averages.

```bash
python main.py expenses.csv
# or explicitly:
python main.py expenses.csv --report category
```

#### 2. Monthly Report

Breaks down spending by month to track trends over time.

```bash
python main.py expenses.csv --report monthly
```

#### 3. Top Expenses Report

Shows the largest individual expenses, useful for identifying major purchases.

```bash
python main.py expenses.csv --report top --top-n 5
```

---

## Examples

### Example 1: Basic Category Summary

Analyze spending patterns across categories using the sample data.

**Command:**
```bash
python main.py examples/sample_expenses.csv
```

**Output:**
```
Category Summary Report
==================================================
Category                    Total    Count        Avg
--------------------------------------------------
Shopping             $     575.00        2 $   287.50
Healthcare           $     500.00        2 $   250.00
Utilities            $     461.00        3 $   153.67
Food                 $     277.54        8 $    34.69
Transportation       $     265.00        3 $    88.33
Entertainment        $     164.99        2 $    82.50
--------------------------------------------------
TOTAL                $   2,243.53       20 $   112.18
```

This shows that Shopping and Healthcare are the largest expense categories, while Food expenses are frequent but smaller on average.

---

### Example 2: Monthly Spending Trends

Track how your spending changes month over month.

**Command:**
```bash
python main.py examples/sample_expenses.csv --report monthly
```

**Output:**
```
Monthly Totals Report
==================================================
Month                  Total    Count        Avg
--------------------------------------------------
2025-01         $     816.79       10 $    81.68
2025-02         $   1,426.74       10 $   142.67
--------------------------------------------------
TOTAL           $   2,243.53       20 $   112.18
```

This reveals that February spending was significantly higher than January (75% increase).

---

### Example 3: Identify Largest Purchases

Find your top 5 biggest expenses.

**Command:**
```bash
python main.py examples/sample_expenses.csv --report top --top-n 5
```

**Output:**
```
Top 5 Expenses Report
================================================================================
Date               Amount Category             Description
--------------------------------------------------------------------------------
2025-02-18 $     450.00 Shopping             New laptop accessory
2025-02-03 $     320.00 Healthcare           Dentist appointment
2025-01-20 $     215.50 Utilities            Electric bill
2025-02-25 $     180.00 Healthcare           Prescription medications
2025-01-12 $     150.00 Utilities            Internet bill
--------------------------------------------------------------------------------
TOTAL (top 5)  $   1,315.50
```

The top 5 expenses alone account for $1,315.50 out of the total $2,243.53 (59% of all spending).

---

### Example 4: Using Your Own Data

Create your own CSV file with your expenses.

**Step 1:** Create a file called `my_expenses.csv`:
```csv
date,amount,category,description
2025-03-01,45.00,Food,Grocery store
2025-03-02,120.00,Transportation,Monthly subway pass
2025-03-05,15.50,Food,Coffee and pastry
2025-03-08,85.00,Utilities,Electric bill
2025-03-10,200.00,Healthcare,Doctor visit
```

**Step 2:** Run the analysis:
```bash
python main.py my_expenses.csv
```

**Step 3:** Try different reports:
```bash
# See monthly breakdown
python main.py my_expenses.csv --report monthly

# See top 3 expenses
python main.py my_expenses.csv --report top --top-n 3
```

---

## Troubleshooting

### "File not found" Error

**Problem:**
```
Error loading data: File not found: my_expenses.csv
```

**Solutions:**
- Check that the file exists: `ls my_expenses.csv` (Mac/Linux) or `dir my_expenses.csv` (Windows)
- Verify you're in the correct directory
- Use the full path to the file: `python main.py /path/to/my_expenses.csv`
- Check for typos in the filename

---

### Invalid CSV Format Errors

**Problem:**
```
Validation error: Invalid data format
```

**Common causes and fixes:**

1. **Missing header row** - Ensure first line is: `date,amount,category,description`

2. **Wrong date format** - Use YYYY-MM-DD format:
   - Correct: `2025-01-15`
   - Wrong: `01/15/2025` or `15-Jan-2025`

3. **Invalid amount** - Use numbers only (no currency symbols):
   - Correct: `42.50`
   - Wrong: `$42.50` or `42.50 USD`

4. **Missing columns** - All four columns required:
   ```csv
   date,amount,category,description
   2025-01-15,42.50,Food,Lunch
   ```

5. **Extra commas or quotes** - Avoid special characters in descriptions or use them carefully:
   - Safe: `Coffee and pastry`
   - Problematic: `Coffee, with cream` (extra comma can split into extra column)
   - Fixed: `"Coffee, with cream"` (quoted if description contains commas)

---

### Empty or No Data Error

**Problem:**
```
No data to report: No valid transactions found in expenses.csv
```

**Solutions:**
- Ensure your CSV has data rows (not just the header)
- Check that all rows have valid data in all four columns
- Verify the file isn't empty: `wc -l expenses.csv` should show more than 1 line

---

### Report Shows Unexpected Results

**Check these common issues:**

1. **Dates not sorting correctly** - Make sure all dates use YYYY-MM-DD format
2. **Categories are case-sensitive** - "Food" and "food" are treated as different categories
3. **Amounts seem wrong** - Check for typos like `4250` instead of `42.50`

---

### Getting Help

To see all available options and examples:

```bash
python main.py --help
```

This displays:
- All command-line options
- Usage examples
- Available report types
- Default values

---

## Tips for Best Results

1. **Consistent categories** - Use the same category names throughout (e.g., always "Food", not sometimes "Food" and sometimes "Groceries")

2. **Accurate dates** - Keep dates in YYYY-MM-DD format for proper sorting and monthly reports

3. **Detailed descriptions** - Write clear descriptions to help identify expenses in top reports

4. **Regular updates** - Update your CSV regularly to track spending trends over time

5. **Backup your data** - Keep copies of your expense CSV files for long-term tracking

---

## Need More Help?

- Review the example file: `examples/sample_expenses.csv`
- Check your Python version: `python --version` (must be 3.8+)
- Ensure you're in the correct directory when running commands
- Try the sample data first to confirm the tool works: `python main.py examples/sample_expenses.csv`
