# Concept 3: Dependency Validation Review

## Exercise Overview

Review file processing code that demonstrates AI-specific red flags, particularly phantom libraries and dependency issues commonly found in AI-generated code.

## Learning Objectives

- Identify AI-specific code patterns and issues
- Learn to validate dependencies and imports
- Recognize phantom libraries that don't exist
- Understand the importance of verifying AI-generated code

## 🤖 AI-Specific Focus

This exercise specifically targets patterns commonly found in AI-generated code. Pay special attention to:
- Library imports and dependencies
- Function signatures and usage
- Context awareness and completeness

## Instructions

### Step 1: Run Phantom Library Detection Tests
```bash
cd concept3-dependency-validation-review/starter
pytest test_phantom_libraries.py -v -s
```

**Expected Output:**
- Import tests reveal dependency issues
- Dependency validation tests demonstrate verification methods
- Tests show patterns for validating external libraries

### Step 2: Review the Code
1. **Open** `starter/file_processor.py` and examine the imports
2. **Apply** the engineering code review framework:
   - Structure & Organization
   - Naming & Clarity
   - Error Handling
   - Dependency Validation
3. **Research any unfamiliar libraries** - verify they exist and are maintained

### Step 3: AI Pattern Detection
4. **Apply** the standard review framework PLUS AI-specific checks:
   - Library names that sound "too good to be true"
   - Generic, appealing names like "advanced" and "pro"
   - Missing documentation or GitHub repos
5. **Check for other issues:**
   - Using `print()` instead of logging
   - Generic exception handling

### Step 4: Run Real Dependencies Tests
```bash
cd ../solution
pytest test_real_dependencies.py -v
```

**Expected Output:**
- All tests pass with real libraries
- Proper error handling demonstrated
- No phantom dependencies detected

### Step 5: Compare and Learn
6. **Compare** the fixed version that uses real, verified libraries

## Review Template

### Dependency Analysis

**Import Verification:**
- [ ] `pandas` - Real library? ✅ / ❌
- [ ] `advanced_file_processor` - Real library? ✅ / ❌
- [ ] `data_cleaner_pro` - Real library? ✅ / ❌
- [ ] Other imports: [List and verify]

**Phantom Library Detection:**
- [ ] Library 1: [Name] - Status: Real / Fake / Uncertain
- [ ] Library 2: [Name] - Status: Real / Fake / Uncertain

### AI-Specific Red Flags

**Missing Context:**
- [ ] Does the code match what was requested?
- [ ] Is any expected functionality missing?
- [ ] Are there unexplained gaps in logic?

**Plausible but Wrong:**
- [ ] Libraries that sound real but aren't
- [ ] Function calls with incorrect signatures
- [ ] Outdated or deprecated patterns

### Code Quality Issues

**Error Handling:**
- [ ] Generic exception handling: [Issues found]
- [ ] Missing specific error types: [What's missing]

**Logging and Debugging:**
- [ ] Using print() instead of logging: [Instances found]
- [ ] Missing debug information: [Areas needing improvement]

### Replacement Recommendations

**For phantom libraries, suggest real alternatives:**
- `advanced_file_processor` → [Your suggestion]
- `data_cleaner_pro` → [Your suggestion]

**For code improvements:**
1. [Specific improvement 1]
2. [Specific improvement 2]
3. [Specific improvement 3]

### Overall Assessment

- **AI Pattern Recognition:** Did you spot the phantom libraries?
- **Quality Rating:** Poor / Fair / Good / Excellent
- **Primary Issue:** Dependency problems / Code quality / Both
- **Recommendation:** Accept / Modify / Reject

## How to Verify Libraries

1. **Check PyPI:** Search for the library on pypi.org
2. **Google Search:** Look for official documentation
3. **GitHub:** Check if there's an active repository
4. **Stack Overflow:** See if others are using it
5. **Package Managers:** Try `pip search` or `conda search`

## Common AI Library Issues

**Phantom Libraries:**
- Libraries that sound plausible but don't exist
- Combinations of real words that seem legitimate
- Outdated libraries that are no longer maintained

**Version Mismatches:**
- Using deprecated APIs
- Mixing different library versions
- Incorrect function signatures

**Context Loss:**
- Missing imports for referenced functions
- Incomplete implementations
- Functions that don't match their names

## Red Flag Patterns

🚩 Libraries with generic, appealing names like:
- `advanced_[something]_processor`
- `[domain]_pro` or `[domain]_master`
- `fast_[operation]` or `quick_[tool]`

🚩 Function calls that seem too convenient:
- Methods with `auto_detect` parameters
- One-line solutions to complex problems
- Perfect APIs that handle everything

After completing your analysis, examine the solution to see how the phantom libraries are replaced with real, well-maintained alternatives, and how proper error handling and logging are implemented.