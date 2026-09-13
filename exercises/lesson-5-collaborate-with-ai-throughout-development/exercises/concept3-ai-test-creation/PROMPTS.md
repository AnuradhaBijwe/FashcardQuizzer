# Concept 3: AI Test Creation

**Exercise Goal**: Generate comprehensive test suite for ReportEngine with unit, integration, and edge case coverage.

## Prompt examples (Adjust as needed)

**Prompt 1** (Comprehensive Test Generation):

```xml
<role>
Senior Python test engineer creating comprehensive test suites
</role>

<task>
Generate complete pytest test suite for ReportEngine class
</task>

<test_requirements>
<test_categories>
1. Basic Functionality (TestReportEngineBasics):
   - Test initialization with loader
   - Test generate_report returns expected structure
   - Test successful report generation with valid data

2. Happy Path Scenarios (TestReportGenerationHappyPath):
   - Test with multiple transactions
   - Test with different report modes (summary, monthly)
   - Test data flows correctly through loader → mode → result

3. Error Handling (TestReportGenerationErrors):
   - Test FileNotFoundError propagates from loader
   - Test ValueError propagates for invalid CSV
   - Test empty transaction list handling
   - Test loader failures handled gracefully

4. Edge Cases (TestEdgeCases):
   - Single transaction
   - Very large transaction list (mock 1000+ items)
   - Special characters in data
</test_categories>

<test_quality_requirements>
- Use pytest fixtures for common test data (sample transactions, mock loaders, mock modes)
- Mock TransactionLoader and ReportMode to isolate ReportEngine testing
- Use pytest.raises for exception testing with error message matching
- Parametrize similar tests (different report modes)
- Clear test names describing what's being tested
- Arrange-Act-Assert structure
- Each test focuses on ONE behavior
</test_quality_requirements>

<test_examples_needed>
Include at least:
- One fixture for sample transaction data
- One fixture for mock loader
- One fixture for mock mode
- One parametrized test showing different report modes
- Exception tests with specific error message assertions
</test_examples_needed>
</test_requirements>

<constraints>
- pytest framework only
- Use unittest.mock for mocking
- No external testing libraries
- Tests must be deterministic (no random data)
- All tests must be independent (no shared state)
</constraints>
```

**Prompt 2** (Edge Case Discovery):

```xml
<task>
Identify additional edge cases for ReportEngine that might not be obvious
</task>

<current_test_coverage>
We have tests for:
- Basic happy path (valid file, successful report)
- Error cases (file not found, invalid data)
- Empty transaction lists
- Single transaction
- Large transaction sets
</current_test_coverage>

<edge_case_analysis>
Consider:
- What happens if loader returns None instead of list?
- What if loader returns list but mode.process_transactions raises unexpected exception?
- What if filepath is empty string or None?
- What if mode returns malformed data structure?
- Race conditions or state management issues?
- Integration edge cases between components?
</edge_case_analysis>

<deliverable>
List 3-5 additional edge case tests we should add.
For each:
- Scenario description
- Expected behavior
- Why it matters
- Brief test outline
</deliverable>
```

**Prompt 3** (Add Critical Edge Cases):

```xml
<task>
Add test cases for two critical edge cases to test_report_engine.py
</task>

<edge_cases_to_add>
1. Test loader returning None instead of list
   - Should raise TypeError with helpful message

2. Test mode.process_transactions raising unexpected exception
   - Should propagate the exception with context
</edge_cases_to_add>

<integration_instructions>
Add to existing test file maintaining same:
- Naming conventions
- Fixture usage
- Documentation style
- Class organization
Provide just the new test methods to add.
</integration_instructions>
```