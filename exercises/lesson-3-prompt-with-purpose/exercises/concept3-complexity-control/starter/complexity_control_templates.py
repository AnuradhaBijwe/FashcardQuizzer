"""
Templates for adding complexity control to structured prompts.

Students will use these templates to prevent over-engineering by adding
appropriate examples and complexity constraints. We use XML as our example 
format, but these principles work with any structured approach.
"""

# Template 1: Name formatting with complexity control
COMPLEXITY_TEMPLATE_1 = """
<task>
Create a function to format user names for display
</task>

<context>
Web application that shows user names in various UI components
Currently concatenating first + last name manually in templates
Need consistent formatting across the application
</context>

<requirements>
- Format names as "First Last" for display
- Handle cases where first or last name might be missing
- Make it reusable across different components
</requirements>

<constraints>
<complexity_limits>
[STUDENT TODO: Set boundaries to prevent over-engineering]
</complexity_limits>

<forbidden_approaches>
[STUDENT TODO: List complex patterns to avoid]
</forbidden_approaches>
</constraints>

<example>
[STUDENT TODO: Show appropriate complexity level for similar functions in the codebase]
</example>
"""

# Template 2: Email validation with scope control
COMPLEXITY_TEMPLATE_2 = """
<task>
Add email validation to user registration form
</task>

<context>
React application with user registration
Currently accepts any input in email field
Need to validate email format before submission
Using formik for form handling
</context>

<requirements>
- Validate email format on form submission
- Show error message for invalid emails
- Prevent form submission if email is invalid
</requirements>

<constraints>
<scope_boundaries>
[STUDENT TODO: Limit scope to prevent complex validation frameworks]
</scope_boundaries>

<complexity_limits>
[STUDENT TODO: Specify appropriate solution size and complexity]
</complexity_limits>

<forbidden_approaches>
[STUDENT TODO: Prevent custom validation frameworks and complex patterns]
</forbidden_approaches>
</constraints>

<example>
[STUDENT TODO: Show similar validation in existing codebase]
</example>
"""

# Template 3: Configuration with simplicity constraints
COMPLEXITY_TEMPLATE_3 = """
<task>
Create configuration for API endpoints
</task>

<context>
Node.js application with multiple API endpoints
Currently hardcoding URLs throughout the codebase
Need centralized configuration for different environments
</context>

<requirements>
- Store API URLs in one place
- Support different URLs for dev/staging/production
- Make it easy to add new endpoints
</requirements>

<constraints>
<simplicity_requirements>
[STUDENT TODO: Specify simple solution requirements]
</simplicity_requirements>

<complexity_limits>
[STUDENT TODO: Set boundaries on configuration complexity]
</complexity_limits>

<forbidden_approaches>
[STUDENT TODO: Prevent complex configuration systems and patterns]
</forbidden_approaches>
</constraints>

<example>
[STUDENT TODO: Show existing simple configuration patterns]
</example>
"""

# Guidance for different constraint types
COMPLEXITY_CONTROL_GUIDANCE = {
    "complexity_limits": {
        "purpose": "Set clear boundaries on solution size and complexity",
        "examples": [
            "Single function, maximum 10 lines",
            "No classes or objects, just pure functions",
            "No more than 2 parameters",
            "Must fit in one file under 50 lines"
        ],
        "pattern_prevention": "Prevents over-engineering by setting explicit size limits"
    },
    "forbidden_approaches": {
        "purpose": "Explicitly prevent complex patterns and architectures",
        "examples": [
            "No design patterns (Strategy, Factory, Observer, etc.)",
            "No abstract base classes or inheritance",
            "No custom framework creation",
            "No configuration systems or dependency injection"
        ],
        "pattern_prevention": "Eliminates over-engineering by forbidding complex solutions"
    },
    "scope_boundaries": {
        "purpose": "Limit the scope of changes to prevent feature creep",
        "examples": [
            "Only modify the specified function/component",
            "No new files or modules",
            "No changes to existing APIs",
            "Focus only on the immediate requirement"
        ],
        "pattern_prevention": "Prevents scope creep that leads to complex solutions"
    },
    "simplicity_requirements": {
        "purpose": "Explicitly require simple, straightforward solutions",
        "examples": [
            "Use the simplest solution that works",
            "Prefer built-in language features over libraries",
            "Keep solution readable by junior developers",
            "No abstractions unless absolutely necessary"
        ],
        "pattern_prevention": "Actively promotes simplicity over complexity"
    }
}

def display_complexity_templates():
    """Display complexity control templates for student completion."""
    templates = [
        ("Template 1: Name Formatting with Complexity Control", COMPLEXITY_TEMPLATE_1),
        ("Template 2: Email Validation with Scope Control", COMPLEXITY_TEMPLATE_2),
        ("Template 3: Configuration with Simplicity Constraints", COMPLEXITY_TEMPLATE_3)
    ]
    
    print("=== COMPLEXITY CONTROL TEMPLATES ===\n")
    print("Add constraints and examples to prevent over-engineering.\n")
    
    for title, template in templates:
        print(f"{title}:")
        print("-" * len(title))
        print(template.strip())
        print("\n" + "="*70 + "\n")

def display_complexity_guidance():
    """Show guidance for different complexity control constraint types."""
    print("=== COMPLEXITY CONTROL GUIDANCE ===\n")
    
    for constraint_type, guidance in COMPLEXITY_CONTROL_GUIDANCE.items():
        print(f"{constraint_type.replace('_', ' ').title()}:")
        print(f"  Purpose: {guidance['purpose']}")
        print(f"  Examples:")
        for example in guidance['examples']:
            print(f"    - {example}")
        print(f"  Pattern Prevention: {guidance['pattern_prevention']}")
        print()

def get_student_completion_checklist():
    """Return checklist for students to verify their complexity control prompts."""
    return {
        "template_1": [
            "Complexity limits specify maximum function size (e.g., 10 lines)",
            "Forbidden approaches prevent design patterns and classes",
            "Example shows simple utility function from existing codebase",
            "Constraints prevent architectural solutions for simple utility"
        ],
        "template_2": [
            "Scope boundaries limit changes to form validation only",
            "Complexity limits specify simple validation approach",
            "Forbidden approaches prevent custom validation frameworks",
            "Example shows existing formik validation patterns"
        ],
        "template_3": [
            "Simplicity requirements explicitly ask for simple solution",
            "Complexity limits prevent configuration management systems",
            "Forbidden approaches prevent complex patterns and abstractions",
            "Example shows simple configuration object from codebase"
        ]
    }

if __name__ == "__main__":
    display_complexity_templates()
    display_complexity_guidance()
    
    print("\n=== COMPLETION CHECKLIST ===")
    checklist = get_student_completion_checklist()
    for template, items in checklist.items():
        print(f"\n{template.replace('_', ' ').title()}:")
        for item in items:
            print(f"  ☐ {item}")