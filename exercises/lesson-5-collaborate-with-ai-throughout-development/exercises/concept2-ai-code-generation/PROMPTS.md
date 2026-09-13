# Concept 2: AI Code Generation

**Exercise Goal**: Generate production-quality TransactionLoader and ReportMode implementations using structured prompts.

## Prompt Examples (Adjust as needed)

**Prompt 1** (Generate TransactionLoader):

```xml
<role>
Senior Python developer implementing planned architecture
</role>

<task>
Implement CSVTransactionLoader class following the interface specification
</task>

<interface_specification>
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class TransactionLoader(ABC):
    @abstractmethod
    def load(self, filepath: str) -> List[Dict[str, Any]]:
        """Load transactions from file.

        Returns:
            List of dicts with keys: date, amount, category, description

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        pass
</interface_specification>

<requirements>
<functionality>
- Implement CSVTransactionLoader inheriting from TransactionLoader
- CSV format: date,amount,category,description (header row required)
- Validate all four fields are present for each row
- Convert amount to float and validate it's positive
- Strip whitespace from all fields
- Provide row-specific error messages for validation failures
</functionality>

<error_handling>
- FileNotFoundError with informative message including filepath
- ValueError for missing columns with specific column names
- ValueError for row-level issues with row number in message
- ValueError for empty/missing required fields
- ValueError for invalid amount (not numeric or negative)
- NO bare except clauses
</error_handling>

<code_quality>
- Comprehensive module and class docstrings
- Method docstrings with Args, Returns, Raises sections
- Full type hints on all signatures
- Use class constant for REQUIRED_COLUMNS
- Extract validation logic to private helper method
- Include usage example in module docstring
</code_quality>
</requirements>

<constraints>
- Python standard library only (csv module)
- Module should be under 150 lines
- Follow PEP 8 style guide
- No external dependencies
</constraints>
```

**Prompt 2** (Generate ReportMode Strategies):

```xml
<task>
Implement two ReportMode strategy classes: SummaryByCategory and MonthlyTotalReport
</task>

<interface_specification>
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ReportMode(ABC):
    @abstractmethod
    def process_transactions(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Process transactions and return report data."""
        pass

    @abstractmethod
    def get_mode_name(self) -> str:
        """Return name of this report mode."""
        pass
</interface_specification>

<requirements>
<strategy_1_summary_by_category>
- Group transactions by 'category' field
- Sum amounts for each category
- Return format: {"mode": "summary", "data": {"Food": 150.50, "Transport": 75.00}, "total": 225.50}
- Handle empty transaction lists (return zero total)
</strategy_1_summary_by_category>

<strategy_2_monthly_total>
- Extract month from 'date' field (format: YYYY-MM-DD, extract YYYY-MM)
- Group transactions by month
- Sum amounts for each month
- Return format: {"mode": "monthly", "data": {"2024-01": 400.00, "2024-02": 350.00}, "total": 750.00}
- Handle empty lists and invalid dates gracefully
</strategy_2_monthly_total>

<both_strategies>
- Follow Strategy pattern (interchangeable implementations)
- Comprehensive docstrings with examples
- Type hints throughout
- Handle edge cases: empty lists, single transaction, duplicate categories/months
- Use defaultdict or similar for clean grouping logic
</both_strategies>
</requirements>

<code_quality>
- Module docstring explaining Strategy pattern usage
- Class docstrings with use cases
- Method docstrings with parameter descriptions
- Clear variable names (no abbreviations)
- Each strategy class under 50 lines
</code_quality>
```

**Prompt 3** (Quick Quality Check):

```xml
<task>
Review the generated transaction_loader.py and report_modes.py for common AI code generation issues from Lesson 2
</task>

<lesson_2_patterns_to_check>
- Phantom dependencies: Are we importing anything that doesn't exist?
- Over-generic code: Is error handling too broad (bare except)?
- Inconsistent patterns: Do similar operations use similar code?
- Missing edge cases: Empty files, single items, duplicates?
- Type safety: Are type hints complete and accurate?
</lesson_2_patterns_to_check>

<action>
List any issues found. If none, confirm code is ready for testing.
</action>
```