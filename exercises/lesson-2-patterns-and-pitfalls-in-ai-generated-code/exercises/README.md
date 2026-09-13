# Lesson 2: Patterns and Pitfalls in AI-Generated Code - Exercises

## Overview

These exercises teach you to recognize common patterns in AI-generated code through hands-on analysis. Each concept focuses on a specific pattern that frequently appears when working with AI coding assistants.

## Exercise Structure

Each exercise follows the same discovery-based approach:
1. **Run failing tests** to see the pattern in action
2. **Analyze the code** using pattern-specific frameworks
3. **Compare with solutions** that address the issues
4. **Learn prevention strategies** for future AI interactions

## Concepts Covered

### Concept 1: Context Gap Pattern
**Pattern:** AI loses track of broader system functionality when focusing on specific requests

**Example Scenario:** AI was asked to add timestamp formatting to a log formatter but removed critical functionality like file logging, monitoring integration, and statistics tracking.

**Key Learning:** Always compare before/after versions line-by-line when AI modifies existing code.

### Concept 2: Phantom Dependencies Pattern  
**Pattern:** AI suggests libraries that sound plausible but don't exist or are outdated

**Example Scenario:** AI creates a name formatter using "name_formatter_pro" and "string_utils_plus" libraries that don't exist, plus deprecated imports like `import String`.

**Key Learning:** Verify all imports against package managers and current documentation before trusting AI suggestions.

### Concept 3: Over-Engineering Pattern
**Pattern:** AI applies complex design patterns to simple problems that don't warrant such complexity

**Example Scenario:** AI was asked to "add logging" to a discount calculation but created an entire strategy pattern implementation with factories, enums, caching, and statistics tracking.

**Key Learning:** Complex patterns should match problem complexity; simple conditionals often suffice.

## Running the Exercises

Navigate to each concept directory and follow the README instructions:

```bash
# Concept 1: Context Gap
cd concept1-context-gap-pattern/starter
pytest test_log_formatter.py -v

# Concept 2: Phantom Dependencies  
cd concept2-phantom-dependencies-pattern/starter
python -m pytest test_name_formatter.py -v

# Concept 3: Over-Engineering
cd concept3-over-engineering-pattern/starter
python -m pytest test_discount_calculator.py -v
```

## Learning Objectives

By completing these exercises, you will:

- **Recognize AI Code Patterns:** Quickly identify common issues in AI-generated code
- **Understand Pattern Origins:** Know why these patterns emerge from AI behavior
- **Apply Systematic Review:** Use pattern knowledge to enhance your code review process
- **Prevent Future Issues:** Understand how to write prompts that avoid these patterns

## Assessment Approach

For each exercise, you should:

1. **Pattern Identification:** Which patterns are present?
2. **Impact Analysis:** What problems do these patterns cause?
3. **Solution Strategy:** How would you address the issues?
4. **Prevention Strategy:** How would you avoid this in future AI interactions?

## Connection to Course Goals

These exercises build on Lesson 1's engineering judgment framework by adding AI-specific pattern recognition. This prepares you for Lesson 3's prompt engineering techniques, where you'll learn to prevent these patterns proactively.

## Time Estimates

- **Concept 1:** 15-20 minutes
- **Concept 2:** 15-20 minutes  
- **Concept 3:** 15-20 minutes
- **Total:** ~60 minutes

## Next Steps

After completing these exercises, you'll be ready to learn proactive strategies for guiding AI toward better code in Lesson 3: Effective Prompt Engineering for Code Generation.
