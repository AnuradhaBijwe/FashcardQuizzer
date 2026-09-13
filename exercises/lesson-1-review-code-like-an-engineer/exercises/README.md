# L1: Review Code Like an Engineer - Exercises

This directory contains hands-on exercises for practicing systematic code review skills and identifying quality issues in unfamiliar code.

## Learning Objectives

By completing these exercises, you will be able to:
- Apply systematic engineering judgment to code review
- Identify quality, readability, and maintainability issues
- Recognize structural and architectural problems
- Spot AI-specific code patterns and red flags
- Provide specific, actionable improvement recommendations

## Engineering Code Review Framework

Use this systematic checklist for all code reviews:

### 1. Structure & Organization
- [ ] Clear separation of concerns
- [ ] Appropriate use of functions/classes
- [ ] Logical code organization

### 2. Naming & Clarity
- [ ] Descriptive variable and function names
- [ ] Self-documenting code
- [ ] Minimal but helpful comments

### 3. Error Handling
- [ ] Proper exception handling
- [ ] Edge case consideration
- [ ] Input validation

### 4. Testability
- [ ] Functions with single responsibilities
- [ ] Minimal external dependencies
- [ ] Predictable behavior

### 5. AI-Specific Checks
- [ ] Are all dependencies real and current?
- [ ] Is existing functionality preserved?
- [ ] Does the context match the request?

## Exercise Structure

Each exercise follows this structure:

```
concept#-exercise-name/
├── starter/
│   └── code_file.py          # Code to review
└── solution/
    └── code_file.py          # Improved version with explanations
```

## Exercises Overview

### Concept 1: Data Processing Review
**File:** `concept1-data-processing-review/`
**Focus:** Basic code quality issues including magic numbers, poor naming, and lack of error handling
**Skills:** Structure analysis, naming conventions, error handling

### Concept 2: Authentication Security Review
**File:** `concept2-authentication-security-review/`
**Focus:** Critical security vulnerabilities and structural issues
**Skills:** Security analysis, SQL injection detection, architecture review

### Concept 3: Dependency Validation Review
**File:** `concept3-dependency-validation-review/`
**Focus:** AI-specific patterns including phantom libraries
**Skills:** Dependency verification, AI pattern recognition, library validation

### Concept 4: API Error Handling Review
**File:** `concept4-api-error-handling-review/`
**Focus:** Basic error handling patterns and network resilience
**Skills:** Error handling analysis, network error management, user experience

### Concept 5: Database Operations Review
**File:** `concept5-database-operations-review/`
**Focus:** Database security and basic SQL injection prevention
**Skills:** Security analysis, query construction review, input validation

## How to Complete Each Exercise

1. **Review the starter code** using the engineering framework above
2. **Identify issues** by category (structure, naming, error handling, etc.)
3. **Look for AI-specific patterns** like phantom libraries or missing functionality
4. **Rate the code quality**: Poor, Fair, Good, Excellent
5. **Make a recommendation**: Accept, Modify, or Reject
6. **Compare with solution** to check your analysis
7. **Review the improved code** to understand best practices

## Assessment Criteria

Your code reviews will be evaluated on:

- **Completeness**: Did you identify all major issues?
- **Categorization**: Can you properly classify issues by type?
- **Specificity**: Are your suggestions concrete and actionable?
- **Security Awareness**: Do you catch security vulnerabilities?
- **AI Pattern Recognition**: Can you identify AI-specific red flags?

## Exercise Completion

Complete all 5 concepts to build systematic code review skills:

1. Review each starter code file using the framework
2. Document all issues found with specific examples
3. Categorize issues by type (structure, naming, error handling, security)
4. Provide specific improvement suggestions
5. Rate overall quality and provide recommendation
6. Compare your analysis with the solution code

## Key Reminders

- **Quality standards are universal** - apply the same criteria regardless of code source
- **Be systematic** - use the checklist to avoid missing issues
- **Focus on maintainability** - consider long-term code health
- **Security first** - always prioritize security issues
- **Verify dependencies** - especially important for AI-generated code

Good luck with your code reviews! Remember, these skills transfer directly to real-world development scenarios.