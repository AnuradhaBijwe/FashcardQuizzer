# Concept 2: Phantom Dependencies Pattern Recognition

## Exercise Overview

Review code that demonstrates the Phantom Dependencies pattern - when AI suggests libraries that sound plausible but don't exist, are outdated, or use incorrect APIs.

**Scenario**: You had a simple, working name formatter (`original_name_formatter.py`) and asked AI to "make the name formatting more robust". AI delivered an "enhanced" version (`name_formatter.py`) with impressive-sounding libraries like "name_formatter_pro" and "string_utils_plus" that don't actually exist.

**Your Task**: Compare the original vs AI-"improved" versions to identify phantom dependencies and broken imports.

## Learning Objectives

- Recognize imports that seem "too good to be true"
- Identify outdated or deprecated library usage patterns
- Understand why AI generates phantom dependencies
- Learn to verify library existence and current API documentation

## Instructions

### Step 1: Run Tests to See the Pattern
```bash
cd concept2-phantom-dependencies-pattern/starter
python -m pytest test_name_formatter.py -v
```

**Expected Output:**
- **Original version tests**: All pass (real dependencies work)
- **AI version import tests**: FAIL (phantom libraries don't exist)
- **Source code analysis tests**: Pass (detecting phantom patterns in code)
- **Comparison tests**: Show how AI broke working code with fake libraries

### Step 2: Review the Code
1. **First, examine the original working code** in `starter/original_name_formatter.py` 
2. **Then, review the AI-"improved" version** in `starter/name_formatter.py`
3. **Compare the two versions** and apply the phantom dependency checklist:
   - What libraries did AI add that don't exist?
   - What deprecated APIs did AI introduce?
   - How did AI make the simple, working code unusable?
4. **Document** your findings using the template below

### Step 3: Run the Solution Tests
```bash
cd ../solution
python -m pytest test_name_formatter.py -v
```

**Expected Output:**
- All tests pass with real, verified dependencies
- Same functionality using legitimate libraries
- Notice how real APIs are properly used

### Step 4: Compare and Learn
4. **Compare** your analysis with the corrected implementation

## Review Template

### Phantom Dependency Analysis

**Suspicious Imports:**
- [ ] Library name: ________________ (Red flags: ________________)
- [ ] Library name: ________________ (Red flags: ________________)
- [ ] Library name: ________________ (Red flags: ________________)

**API Usage Issues:**
- [ ] Function: ________________ (Issue: ________________)
- [ ] Function: ________________ (Issue: ________________)

**Verification Results:**
- [ ] Checked package manager (pip/npm): ________________
- [ ] Checked official documentation: ________________
- [ ] Checked current API signatures: ________________

### Pattern Recognition

**Phantom Dependency Indicators:**
- [ ] Library names with "pro", "advanced", "fast", "super" prefixes
- [ ] Imports that seem too convenient or comprehensive
- [ ] Deprecated modules from old documentation
- [ ] Function calls that don't match current API docs

### Impact Assessment

**Immediate Impact:**
- [ ] Code won't run due to import errors
- [ ] Dependencies can't be installed
- [ ] Function signatures don't match

**Long-term Impact:**
- [ ] Technical debt from incorrect assumptions
- [ ] Security risks from unvetted libraries
- [ ] Maintenance burden from deprecated APIs

### Recommendations

1. **Verification Strategy:** [How to check if libraries exist]
2. **Alternative Libraries:** [Real libraries that provide similar functionality]
3. **API Validation:** [How to verify current API signatures]

### Overall Assessment

- **Pattern Confidence:** Low / Medium / High
- **Recommendation:** Accept / Modify / Reject
- **Reasoning:** [Your explanation]

## Key Learning Points

- Always verify that imported libraries actually exist before using AI suggestions
- Check package managers and official documentation for current API signatures
- Be suspicious of library names that sound "too good to be true"
- AI training data includes code from different time periods, leading to outdated suggestions

## Common Red Flags for Phantom Dependencies

1. **Convenient Names:** Libraries with "advanced", "pro", "fast", "super" in the name
2. **Perfect Fit:** Imports that seem exactly tailored to your use case
3. **Deprecated Paths:** Old import paths from outdated documentation
4. **Version Mismatches:** Function signatures that don't match current library versions
5. **Missing Context:** Libraries used without proper setup or configuration

After completing your review, check the solution to see how the same functionality can be achieved using real, well-documented libraries with proper API usage.