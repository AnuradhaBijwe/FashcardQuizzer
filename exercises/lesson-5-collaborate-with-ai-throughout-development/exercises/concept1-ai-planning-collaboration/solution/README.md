# Concept 2: AI Code Generation

## Learning Objectives
- Generate quality Python modules using AI
- Write effective prompts that specify interfaces and constraints
- Review and refine AI-generated code
- Ensure generated code includes type hints, docstrings, and error handling

## Exercise Overview

In this exercise, you'll practice using AI to generate complete, production-quality Python modules. You'll learn how to:
1. Break down generation into focused, manageable prompts
2. Specify clear interfaces and requirements
3. Request proper error handling and validation
4. Ensure code quality through iteration

## Part A: Guided Exercise (Expense Tracker)

### Context
You've completed architectural planning (Concept 1) and now have interfaces defined. Your task is to generate implementations for:
1. **TransactionLoader** - CSV loading with validation
2. **ReportMode Strategies** - Different report types

### Step 1: Generate TransactionLoader

Create `transaction_loader.py` that implements the TransactionLoader interface.

**Requirements**:
- Loads CSV files with columns: date, amount, category, description
- Validates all required fields are present
- Converts amount to float, validates it's positive
- Handles FileNotFoundError gracefully
- Handles malformed CSV data with clear error messages
- Returns List[Dict[str, Any]]
- Includes comprehensive docstrings and type hints

<prompt_template>
<task>
Generate a Python module transaction_loader.py that implements CSV transaction loading with validation
</task>

<interface>
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class TransactionLoader(ABC):
    @abstractmethod
    def load(self, filepath: str) -> List[Dict[str, Any]]:
        """Load transactions from file."""
        pass
</interface>

<requirements>
- Implement CSVTransactionLoader class that inherits from TransactionLoader
- Load CSV with columns: date, amount, category, description
- Validate all fields are present for each transaction
- Convert amount to float and ensure it's positive
- Handle FileNotFoundError with informative message
- Handle malformed CSV (bad format, missing columns) with ValueError
- Include comprehensive docstrings with examples
- Use full type hints throughout
- Follow Python best practices
</requirements>

<constraints>
- Use only Python standard library (csv module)
- No external dependencies
- Include at least one usage example in module docstring
</constraints>
</prompt_template>

**Expected Deliverable**: `transaction_loader.py` with CSVTransactionLoader class

### Step 2: Generate ReportMode Strategies

Create `report_modes.py` that implements different report strategies.

**Requirements**:
- Implements ReportMode interface from planning exercise
- Two strategy classes: SummaryByCategory and MonthlyTotalReport
- SummaryByCategory: Groups transactions by category, sums amounts
- MonthlyTotalReport: Groups by month (from date field), sums amounts
- Clear, descriptive output format
- Handles empty transaction lists
- Comprehensive type hints and docstrings

<prompt_template>
<task>
Generate report_modes.py implementing Strategy pattern for different report types
</task>

<interface>
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
</interface>

<requirements>
Strategy 1: SummaryByCategory
- Groups transactions by 'category' field
- Sums amounts for each category
- Returns dict with structure: {"mode": "summary", "data": {"Food": 150.50, ...}, "total": 500.00}

Strategy 2: MonthlyTotalReport  
- Extracts month from 'date' field (format: YYYY-MM-DD)
- Groups transactions by month
- Sums amounts for each month
- Returns dict with structure: {"mode": "monthly", "data": {"2024-01": 400.00, ...}, "total": 1200.00}

Both strategies:
- Handle empty transaction lists (return appropriate empty structure)
- Include descriptive docstrings
- Use full type hints
- Follow Strategy pattern properly
</requirements>
</prompt_template>

**Expected Deliverable**: `report_modes.py` with both strategy classes

### Step 3: Review and Refine

After generating code, review it against this checklist:

**Code Quality Checklist**:
- [ ] All classes have docstrings explaining purpose
- [ ] All methods have docstrings with params and return values
- [ ] Type hints on all function signatures
- [ ] Error handling is specific (not bare except:)
- [ ] Error messages are informative
- [ ] No magic numbers or strings
- [ ] Variable names are descriptive
- [ ] Follows PEP 8 style guide
- [ ] Includes usage examples in docstrings

**Functionality Checklist**:
- [ ] Implements required interfaces correctly
- [ ] Handles all specified error cases
- [ ] Returns data in expected format
- [ ] Works with empty inputs gracefully
- [ ] No unnecessary dependencies

If any items are missing, refine your prompts and regenerate.

## Part B: Apply to Your Project

Now apply the same process to your own project:

1. **Choose 2-3 modules** from your architecture plan
2. **Write generation prompts** using the XML template structure
3. **Generate implementations** with AI
4. **Review against checklists** above
5. **Refine and iterate** until quality standards met

**Deliverable**: Working implementations with tests

## Validation

Your code will be tested for:
- **Correctness**: Implements interfaces properly
- **Error Handling**: Handles specified error conditions
- **Code Quality**: Includes docstrings, type hints, follows best practices
- **Functionality**: Produces expected outputs

Run tests:
```bash
pytest test_transaction_loader.py -v
pytest test_report_modes.py -v
```

## Key Takeaways

- Breaking generation into focused modules produces better results
- Specifying interfaces and constraints upfront prevents issues
- Quality checklists ensure AI output meets standards
- Iteration improves code quality significantly
- The same prompts can be adapted to any project domain

## Time Estimate
40-50 minutes
