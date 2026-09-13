# Concept 4: AI Refactoring Collaboration

**Exercise Goal**: Improve cli interface by reducing duplication, adding type safety, and extracting constants, while keeping all tests passing.

## Prompt Examples (Adjust as needed)

**Prompt 1** (Identify Refactoring Opportunities):

```xml
<role>
Senior software engineer performing code review
</role>

<task>
Analyze cli interface implementation and identify specific refactoring opportunities
</task>

<analysis_framework>
Review for:

1. Duplication
   - Repeated code blocks
   - Similar error handling patterns
   - Duplicated formatting logic

2. Magic Values
   - Hard-coded strings (especially color codes)
   - Hard-coded numbers
   - Repeated literals

3. Type Safety
   - Missing type hints
   - Incomplete type annotations
   - Any types that could be more specific

4. Complexity
   - Methods doing multiple things
   - Long methods (>30 lines)
   - Deeply nested logic

5. Code Smells
   - Inconsistent naming
   - Poor separation of concerns
   - Unclear method purposes
</analysis_framework>

<output_format>
For each issue found:
- Line numbers or method name
- Category (duplication, magic values, etc.)
- Current code snippet
- Suggested improvement
- Benefit of change
- Refactoring risk (LOW/MEDIUM/HIGH)
</output_format>
```

**Prompt 2** (Apply Safe Refactorings):

```xml
<task>
Create a new version of the cli interface on a new versioned file with refactorings applied
</task>


<refactorings_to_apply>
1. Extract all color codes into class constants (LOW risk)
   - Create Color class or constants: RESET, RED, GREEN, BLUE, YELLOW
   - Replace all "\033[..." literals with named constants

2. Create helper method for error formatting (LOW risk)
   - Extract repeated error formatting into _format_error_message(msg: str) -> str
   - Use in all error display methods

3. Add complete type hints (LOW risk)
   - Add return type hints to all methods
   - Add parameter type hints where missing
   - Import typing as needed

4. Extract report formatting (MEDIUM risk)
   - Split display_report into smaller focused methods
   - _format_header, _format_row, _format_footer
   - Maintain exact same output format
</refactorings_to_apply>

<critical_constraints>
- ALL existing tests must pass WITHOUT modification
- Public API must remain identical (method signatures unchanged)
- Output format must be EXACTLY the same
- No behavior changes - only structure improvements
- Keep same error messages (tests may check them)
- Maintain backward compatibility completely
</critical_constraints>

<quality_requirements>
- Add docstrings to new helper methods
- Keep code PEP 8 compliant
- Preserve existing comments if they explain "why"
- Update class docstring to mention constants
</quality_requirements>
```

**Prompt 3** (Document Refactoring):

```xml
<task>
Create refactoring_notes.md documenting the changes made
</task>

<refactorings_completed>
1. Extracted color codes to constants
2. Created _format_error_message helper
3. Added complete type hints
4. Split display_report into smaller methods
</refactorings_completed>

<documentation_format>
# Refactoring Notes: CLI Interface v1 → v2

## Summary
[One paragraph: what was refactored and why]

## Changes Applied

### [Change Name]
- **What**: [Specific code change]
- **Why**: [Problem it solved]
- **Benefit**: [Measurable improvement]
- **Risk**: [Was it risky? What could have gone wrong?]
- **Validation**: [How we verified it worked]

[Repeat for each change]

## Metrics Comparison
| Metric | v1 | v2 | Improvement |
|--------|----|----|-------------|
| Lines of code | X | Y | Z |
| Magic strings | X | Y | Z |
| Type hint coverage | X% | Y% | Z% |
| Longest method | X lines | Y lines | Z lines |

## Testing
- All original tests pass: ✓
- No behavior changes: ✓
- Backward compatible: ✓
</documentation_format>
```