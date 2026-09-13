# Concept 3: Complexity Control

**Exercise Goal**: Use structured prompts to prevent over-engineering and maintain appropriate complexity levels.

**Prompt 1** (Structured Approach):
```xml
<task>
Add logging to discount calculation function
</task>

<existing_code>
def calculate_discount(price, customer_type):
    if customer_type == 'premium':
        return price * 0.15
    elif customer_type == 'regular':
        return price * 0.05
    else:
        return 0.0
</existing_code>

<requirements>
- Add exactly 2 log statements: function entry and result
- Log should include price, customer_type, and calculated discount
- Use Python's standard logging module
- Handle invalid customer types appropriately
</requirements>

<constraints>
<complexity_limits>
- Keep as a single function (no classes)
- Maximum 15 lines of code
- No design patterns (no Strategy, no Factory)
- No abstract base classes or enums
</complexity_limits>

<forbidden_approaches>
- No object-oriented refactoring
- No splitting into multiple classes
- No configuration classes
- Simple is better than complex
</forbidden_approaches>
</constraints>

<example>
Similar utility function from our codebase:
```python
def calculate_tax(amount, rate):
    logger.info(f"Calculating tax: amount={amount}, rate={rate}")
    if amount <= 0:
        logger.warning("Invalid amount for tax calculation")
        return 0.0
    result = round(amount * rate, 2)
    logger.info(f"Tax calculated: {result}")
    return result
```
</example>
```

**Prompt 2** (Verify Simplicity):
```xml
<task>
Review this discount calculator for appropriate complexity
</task>

<evaluation_criteria>
- Is it a single, simple function?
- Does it solve only the stated requirements?
- Could a junior developer understand it immediately?
- Is it easy to test?
- Does it avoid unnecessary abstractions?
</evaluation_criteria>
```

**Prompt 3** (Document When Complexity IS Warranted):
```xml
<task>
Document when you WOULD increase complexity for discount calculations
</task>

<context>
Help the team understand when the current simple approach should evolve
</context>

<questions>
1. How many discount types would justify using a pattern?
2. What complexity in discount rules would require abstraction?
3. What future requirements would necessitate refactoring?
</questions>
```