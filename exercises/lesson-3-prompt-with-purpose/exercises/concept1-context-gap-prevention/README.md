# Concept 1: Context Gap Prevention

## Exercise Overview

Learn to use XML structure to prevent the context gap pattern where AI focuses on new requirements but loses existing functionality.

**Scenario**: You have prompts for modifying existing code, but AI often removes or changes functionality beyond the requested scope. Your task is to use XML structure to make preservation requirements explicit.

**Your Task**: Create XML prompts that prevent AI from losing existing functionality when adding new features.

## Learning Objectives

- Master XML tags for preserving context (`<existing_code>`, `<requirements>`, `<thinking>`)
- Prevent the context gap pattern from Lesson 2
- Make functionality preservation explicit in prompts
- Use structured thinking to guide AI reasoning about existing code

## Instructions

### Step 1: Review Traditional Prompts
```bash
cd concept1-basic-xml-structure/starter
python review_prompts.py
```

**What you'll see:**
- 3 traditional prompts with common structural problems
- AI responses that demonstrate the issues with unstructured prompts
- Clear examples of ambiguity and missing context

### Step 2: Practice XML Conversion
1. **Examine** the traditional prompts in `starter/traditional_prompts.py`
2. **Convert** each prompt using the XML template in `starter/xml_templates.py`
3. **Test** your XML prompts using `starter/prompt_tester.py`
4. **Compare** outputs between traditional and XML versions

### Step 3: Run the Tests
```bash
pytest test_prompt_structure.py -v
```

**Expected Output:**
- **Structure tests**: Verify your XML prompts use proper tags
- **Clarity tests**: Check that requirements are explicit
- **Completeness tests**: Ensure context and constraints are included

### Step 4: Compare with Solution
```bash
cd ../solution
python review_prompts.py
pytest test_prompt_structure.py -v
```

## Exercise Template

### Traditional Prompt Analysis

For each prompt, identify:
- **Ambiguity Issues**: What could be interpreted multiple ways?
- **Missing Context**: What background information is assumed?
- **Unclear Requirements**: What specific outcomes are expected?
- **Constraint Gaps**: What limitations aren't specified?

### XML Conversion Checklist

- [ ] `<task>` clearly states the specific objective
- [ ] `<context>` provides necessary background information
- [ ] `<requirements>` lists explicit, testable outcomes
- [ ] `<constraints>` specifies limitations and boundaries

### Quality Assessment

Rate your XML prompts on:
- **Clarity**: Can AI understand exactly what's needed?
- **Completeness**: Are all necessary details included?
- **Specificity**: Are requirements measurable and testable?
- **Structure**: Does XML organization improve comprehension?

## Key Learning Points

- XML structure prevents information loss that occurs in conversational prompts
- Clear separation of task, context, and requirements improves AI accuracy
- Structured prompts are easier to iterate and improve
- Basic XML tags create the foundation for advanced prompt engineering

## Success Criteria

After this exercise, you should be able to:
1. Identify structural problems in traditional prompts
2. Convert conversational prompts to basic XML format
3. Use `<task>`, `<context>`, and `<requirements>` tags effectively
4. Demonstrate measurable improvement in AI output quality

Progress to Concept 2 to learn advanced constraint techniques for preventing phantom dependencies.