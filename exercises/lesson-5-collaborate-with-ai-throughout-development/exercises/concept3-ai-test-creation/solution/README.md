# Concept 4: AI Refactoring Collaboration

## Learning Objectives
- Use AI to identify refactoring opportunities systematically
- Apply refactorings while maintaining correctness (tests must pass)
- Improve code quality metrics (complexity, duplication, type safety)
- Evaluate refactoring impact objectively

## Exercise Overview

In this exercise, you'll practice using AI to improve existing working code. You'll learn how to:
1. Identify code smells and improvement opportunities
2. Apply refactorings incrementally with test validation
3. Measure improvement objectively
4. Maintain backward compatibility

## Part A: Guided Exercise (Expense Tracker)

### Context
You have a working `cli_interface_v1.py` module that displays reports in the terminal. It works, but has room for improvement:
- Repetitive error handling patterns
- Some magic values
- Inconsistent formatting
- Could use better type safety

Your task: Refactor to improve quality while keeping all tests passing.

### Step 1: Analyze Current Code

Review `cli_interface_v1.py` and identify issues:

**Code Smells**:
- Duplicated error formatting logic
- Magic strings for colors/formatting
- Repetitive try-except patterns
- Missing type hints in some places
- Long methods doing multiple things

### Step 2: Run Baseline Tests

Before refactoring, verify everything works:

```bash
pytest test_cli_interface.py -v
```

All tests should pass. These tests MUST continue passing after refactoring.

### Step 3: Identify Refactoring Opportunities with AI

Use AI to systematically identify improvements:

<prompt_template>
<task>
Analyze cli_interface_v1.py and identify refactoring opportunities
</task>

<code>
[Paste cli_interface_v1.py content]
</code>

<analysis_framework>
For each method, evaluate:
1. Single Responsibility: Does it do one thing?
2. Duplication: Is logic repeated elsewhere?
3. Magic Values: Are there hardcoded strings/numbers that should be constants?
4. Error Handling: Is it consistent and comprehensive?
5. Type Safety: Are type hints complete and accurate?
6. Complexity: Is it easy to understand and test?
</analysis_framework>

<output_format>
List each refactoring opportunity with:
- Location (method/line)
- Issue category (duplication, magic values, etc.)
- Suggested improvement
- Expected benefit
- Risk level (low/medium/high)
</output_format>
</prompt_template>

### Step 4: Apply Refactorings Incrementally

Apply improvements one at a time, running tests after each:

<prompt_template>
<task>
Refactor cli_interface_v1.py to create cli_interface_v2.py with specified improvements
</task>

<current_code>
[Paste cli_interface_v1.py]
</current_code>

<refactorings_to_apply>
1. Extract color codes into class constants
2. Create helper method for error message formatting
3. Extract report formatting logic into separate methods
4. Add complete type hints
5. Reduce method complexity by extracting sub-operations
</refactorings_to_apply>

<constraints>
- All existing tests MUST pass without modification
- Maintain exact same public API
- No behavior changes - only structure improvements
- Add docstrings where missing
- Follow existing code style
</constraints>

<validation>
After each refactoring:
1. Run: pytest test_cli_interface.py -v
2. Verify all tests still pass
3. Check complexity metrics improved
</validation>
</prompt_template>

**Expected Deliverable**: `cli_interface_v2.py` with improvements

### Step 5: Measure Improvement

The exercise includes `test_refactoring_improvements.py` which validates:
- Reduced code duplication
- Proper use of constants (no magic values)
- Improved type coverage
- Methods are more focused (lower complexity)

```bash
pytest test_refactoring_improvements.py -v
```

Also document changes:

<prompt_template>
<task>
Document the refactoring changes made to cli_interface
</task>

<format>
For each refactoring:
- What: Specific change made
- Why: Problem it solves
- Benefit: Measurable improvement
- Risk: Any potential issues
</format>

<metrics>
Include before/after comparison:
- Lines of code
- Number of methods
- Cyclomatic complexity
- Type hint coverage
- Test coverage
</metrics>
</prompt_template>

Save as `refactoring_notes.md`

## Part B: Apply to Your Project

Now apply the same process to your own code:

1. **Choose a module** that works but could be better
2. **Run existing tests** to establish baseline
3. **Analyze with AI** using the framework above
4. **Apply refactorings incrementally**, testing after each
5. **Measure improvements** objectively
6. **Document changes** with rationale

**Deliverable**: Refactored module with passing tests and documentation

## Validation

Your refactoring will be validated for:
- **Correctness**: All original tests still pass
- **Improvement**: Metrics show measurable benefits
- **Documentation**: Changes are clearly explained
- **Safety**: No behavior changes, only structure improvements

Run tests:
```bash
pytest test_cli_interface.py -v
pytest test_refactoring_improvements.py -v
```

## Key Takeaways

- Always refactor with a test safety net
- Apply changes incrementally, not all at once
- Measure improvements objectively with metrics
- AI can identify patterns humans miss
- Documentation captures the "why" of changes
- Maintain backward compatibility unless explicitly changing API

## Time Estimate
30-40 minutes
