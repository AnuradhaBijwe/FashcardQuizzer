# Concept 3: AI Test Creation

## Learning Objectives
- Generate comprehensive test suites using AI
- Identify test scenarios systematically (happy path, errors, edge cases)
- Evaluate test quality and completeness
- Use AI to discover edge cases you might miss

## Exercise Overview

In this exercise, you'll practice using AI to generate high-quality tests. You'll learn how to:
1. Prompt for specific test categories (unit, integration, edge cases)
2. Request proper test structure with fixtures and mocks
3. Ensure tests verify behavior, not implementation details
4. Achieve appropriate test coverage

## Part A: Guided Exercise (Expense Tracker)

### Context
You have a working `report_engine.py` module that needs comprehensive tests. Your task is to generate a complete test suite that validates all functionality.

### The Module to Test

The `report_engine.py` file contains:
- `ReportEngine` class that orchestrates report generation
- Uses `TransactionLoader` to load data
- Uses `ReportMode` strategies to process data
- Handles errors at each step

Your job: Generate comprehensive tests for this module.

### Step 1: Analyze Test Requirements

Before generating tests, identify what needs testing:

**Happy Path Scenarios**:
- Loading valid data and generating reports successfully
- Using different report modes (summary, monthly)
- Correct data flow through the system

**Error Scenarios**:
- File not found
- Invalid CSV data
- Empty transaction lists
- Loader failures
- Strategy failures

**Edge Cases**:
- Very large transaction files
- Single transaction
- Multiple transactions same category/month
- Special characters in data

### Step 2: Generate Test Suite

Use AI to generate `test_report_engine.py` that covers all scenarios.

<prompt_template>
<task>
Generate comprehensive pytest test suite for ReportEngine class
</task>

<module_to_test>
# ReportEngine orchestrates report generation
# Uses TransactionLoader to load CSV data
# Uses ReportMode strategies to process transactions
# Returns formatted report data or raises errors

class ReportEngine:
    def __init__(self, loader: TransactionLoader):
        self.loader = loader
    
    def generate_report(self, filepath: str, mode: ReportMode) -> Dict[str, Any]:
        # Load transactions
        # Process with mode strategy
        # Return results
        pass
</module_to_test>

<requirements>
Test Categories:
1. Happy path tests
   - Successful report generation with valid data
   - Different report modes work correctly
   - Correct data transformation

2. Error handling tests
   - FileNotFoundError from loader
   - ValueError from invalid data
   - Empty transaction lists handled gracefully

3. Integration tests
   - Full flow from file to report
   - Multiple report modes
   - Real file I/O scenarios

4. Edge cases
   - Single transaction
   - Very large files (mock with many transactions)
   - Special characters in data

Test Quality Requirements:
- Use pytest fixtures for reusable test data
- Mock external dependencies (file I/O)
- Test behavior, not implementation
- Clear, descriptive test names
- Comprehensive docstrings
- Proper assertions with error messages
- Use parametrize for similar test variations
</requirements>

<test_structure>
- TestReportEngineBasics: Instantiation, basic functionality
- TestReportGenerationHappyPath: Successful report generation scenarios
- TestReportGenerationErrors: Error handling and edge cases
- TestIntegration: Full end-to-end workflows
</test_structure>
</prompt_template>

**Expected Deliverable**: `test_report_engine.py` with comprehensive test coverage

### Step 3: Evaluate Test Quality

After generating tests, evaluate them against this checklist:

**Coverage Checklist**:
- [ ] All public methods tested
- [ ] Happy path scenarios covered
- [ ] Error scenarios tested with proper exception assertions
- [ ] Edge cases identified and tested
- [ ] Integration scenarios included

**Quality Checklist**:
- [ ] Tests use fixtures for common setup
- [ ] External dependencies properly mocked
- [ ] Test names clearly describe what's being tested
- [ ] Each test focuses on one thing
- [ ] Assertions include failure messages
- [ ] No test interdependencies

**Best Practices Checklist**:
- [ ] Tests are deterministic (same result every run)
- [ ] No hard-coded file paths
- [ ] Proper setup and teardown
- [ ] Tests run quickly
- [ ] Clear arrange-act-assert structure

### Step 4: Run Quality Validation

The starter includes `validate_test_quality.py` which meta-tests your test suite:

```bash
pytest validate_test_quality.py -v
```

This validates:
- Required test classes exist
- Minimum number of tests present
- Tests use fixtures appropriately
- Tests use mocking for dependencies
- Test naming conventions followed

## Part B: Apply to Your Project

Now apply the same process to your own project:

1. **Choose a module** from your implementation that needs tests
2. **Analyze test requirements** (happy path, errors, edge cases)
3. **Write a generation prompt** using the XML template structure
4. **Generate the test suite** with AI
5. **Evaluate quality** against the checklists above
6. **Run and refine** until all tests pass and quality standards met

**Deliverable**: Complete test suite with >80% coverage

## Validation

Your tests will be validated for:
- **Completeness**: All scenarios covered
- **Quality**: Proper structure, fixtures, mocks
- **Correctness**: Tests actually test the right things
- **Maintainability**: Clear, well-organized, independent tests

Run tests:
```bash
pytest test_report_engine.py -v
pytest validate_test_quality.py -v
```

## Key Takeaways

- AI can identify test scenarios you might miss
- Structured prompts produce better organized test suites
- Quality evaluation is essential - first generation is rarely perfect
- Good tests test behavior, not implementation details
- Fixtures and mocks make tests cleaner and faster

## Time Estimate
30-40 minutes
