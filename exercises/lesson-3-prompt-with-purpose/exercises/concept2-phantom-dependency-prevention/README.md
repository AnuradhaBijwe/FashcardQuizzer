# Concept 2: Phantom Dependency Prevention

## Exercise Overview

Learn to use XML constraint techniques to prevent AI from suggesting non-existent libraries and dependencies.

**Scenario**: AI keeps suggesting libraries that don't exist in your environment or aren't available in your project. Your task is to use constraint tags to explicitly define what libraries are available and prevent phantom dependencies.

**Your Task**: Create constraint structures that eliminate AI suggestions of non-existent libraries and dependencies.

## Learning Objectives

- Master `<allowed_libraries>`, `<forbidden_approaches>`, and `<constraints>` tags
- Prevent the phantom dependency pattern from Lesson 2
- Explicitly define available vs. unavailable dependencies
- Create constraints that guide AI toward implementable solutions

## Instructions

### Step 1: Review Problem Prompts
```bash
cd concept2-constraint-prevention/starter
python analyze_problems.py
```

**What you'll see:**
- XML prompts that lack proper constraints
- Simulated AI responses showing phantom dependency issues
- Over-engineering patterns that result from unconstrained prompts

### Step 2: Practice Constraint Design
1. **Examine** the problematic prompts in `starter/problem_prompts.py`
2. **Identify** what constraints are missing using `starter/constraint_analyzer.py`
3. **Add** appropriate constraint tags using templates in `starter/constraint_templates.py`
4. **Test** your enhanced prompts using `starter/constraint_tester.py`

### Step 3: Run Prevention Tests
```bash
pytest test_constraint_effectiveness.py -v
```

**Expected Output:**
- **Phantom dependency prevention**: Verify constraints eliminate invalid library suggestions
- **Complexity control tests**: Check that constraints prevent over-engineering
- **Architecture compatibility tests**: Ensure constraints maintain system integration

### Step 4: Compare with Solution
```bash
cd ../solution
python analyze_problems.py
pytest test_constraint_effectiveness.py -v
```

## Exercise Template

### Problem Pattern Analysis

For each problematic prompt, identify:
- **Phantom Dependency Risk**: What non-existent libraries might AI suggest?
- **Over-Engineering Risk**: Where might AI add unnecessary complexity?
- **Architecture Mismatch Risk**: What solutions wouldn't fit existing systems?
- **Missing Constraint Types**: What boundaries need to be set?

### Constraint Design Checklist

- [ ] `<allowed_libraries>` explicitly lists available dependencies
- [ ] `<forbidden_approaches>` prevents problematic patterns
- [ ] `<complexity_limits>` sets appropriate solution boundaries
- [ ] `<integration_requirements>` specifies system compatibility needs
- [ ] `<performance_constraints>` defines efficiency requirements

### Quality Assessment

Rate your constraint-enhanced prompts on:
- **Phantom Prevention**: Do constraints eliminate invalid dependencies?
- **Complexity Control**: Do constraints prevent over-engineering?
- **Architecture Fit**: Do constraints ensure system compatibility?
- **Specificity**: Are constraints measurable and testable?

## Key Learning Points

- Explicit constraints prevent AI from hallucinating non-existent solutions
- Complexity limits guide AI toward appropriately-scoped implementations
- Forbidden approaches eliminate patterns that cause integration problems
- Well-designed constraints improve AI output reliability and system fit

## Success Criteria

After this exercise, you should be able to:
1. Identify constraint gaps that lead to phantom dependencies
2. Design effective constraint structures using multiple tag types
3. Prevent over-engineering through complexity boundaries
4. Create constraints that ensure architectural compatibility

Progress to Concept 3 to learn advanced example and thinking tag techniques.