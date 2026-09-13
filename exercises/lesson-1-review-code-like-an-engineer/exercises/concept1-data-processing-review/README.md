# Concept 1: Data Processing Review

## Exercise Overview

Review a data processing function that demonstrates common code quality issues including magic numbers, poor naming conventions, and lack of error handling.

## Learning Objectives

- Identify structural and organizational issues
- Recognize poor naming conventions
- Spot missing error handling
- Understand the importance of avoiding magic numbers

## Instructions

### Step 1: Run Tests to See the Issues
```bash
cd concept1-data-processing-review/starter
pytest test_data_processor.py -v
```

**Expected Output:**
- Basic functionality tests pass
- Error handling tests FAIL (demonstrating missing error handling!)
- Shows magic numbers and poor naming issues

### Step 2: Review the Code
1. **Open** `starter/data_processor.py` and review the function
2. **Apply** the engineering code review framework:
   - Structure & Organization
   - Naming & Clarity
   - Error Handling
   - Testability
3. **Document** your findings using the template below

### Step 3: Run the Solution Tests
```bash
cd ../solution
pytest test_data_processor.py -v
```

**Expected Output:**
- All tests pass showing fixes work
- Error handling now works gracefully
- Notice improved testability with constants

### Step 4: Compare and Learn
4. **Compare** your analysis with the improved code

## Review Template

### Issues Found

**Structure & Organization:**
- [ ] Issue 1: [Description]
- [ ] Issue 2: [Description]

**Naming & Clarity:**
- [ ] Issue 1: [Description]
- [ ] Issue 2: [Description]

**Error Handling:**
- [ ] Issue 1: [Description]
- [ ] Issue 2: [Description]

**Testability:**
- [ ] Issue 1: [Description]
- [ ] Issue 2: [Description]

### Specific Recommendations

1. **Magic Numbers:** [Your recommendations]
2. **Variable Naming:** [Your recommendations]
3. **Error Handling:** [Your recommendations]
4. **Function Design:** [Your recommendations]

### Overall Assessment

- **Quality Rating:** Poor / Fair / Good / Excellent
- **Recommendation:** Accept / Modify / Reject
- **Reasoning:** [Your explanation]

## Key Learning Points

- Magic numbers make code unmaintainable
- Poor variable names reduce code readability
- Missing error handling leads to runtime failures
- Functions should have single, clear responsibilities

## Common Issues to Look For

1. **Magic numbers** (1.2, 100) without explanation
2. **Generic variable names** ('temp', 'data')
3. **No input validation** for missing keys
4. **Mixed responsibilities** in single function
5. **Hard-coded values** scattered throughout

After completing your review, check the solution to see the improved version with proper constants, descriptive names, comprehensive error handling, and separated concerns.