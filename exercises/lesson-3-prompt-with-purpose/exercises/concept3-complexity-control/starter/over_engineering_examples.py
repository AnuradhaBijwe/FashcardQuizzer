"""
Examples of prompts that lead to over-engineering patterns.

These prompts lack proper examples and complexity controls, causing AI to create
unnecessarily complex solutions for simple tasks.
"""

# Over-Engineering Example 1: Simple utility function becomes complex architecture
OVER_ENGINEERED_PROMPT_1 = """
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
- Must be maintainable and extensible
- Should follow good software engineering practices
</constraints>
"""

# Over-Engineering Example 2: Simple validation becomes complex system
OVER_ENGINEERED_PROMPT_2 = """
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
- Should integrate with existing formik setup
- Must be robust and handle edge cases
</constraints>
"""

# Over-Engineering Example 3: Simple configuration becomes complex pattern
OVER_ENGINEERED_PROMPT_3 = """
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
- Should be scalable for future growth
- Must be enterprise-ready
</constraints>
"""

# What these prompts typically produce (over-engineered solutions)
TYPICAL_AI_RESPONSES = {
    "prompt_1_problems": [
        "Complex NameFormatter class with multiple methods",
        "Strategy pattern for different name formats",
        "Abstract base class for formatter types", 
        "Factory pattern to create formatters",
        "Configuration system for formatting rules",
        "Custom exceptions for name validation errors"
    ],
    "prompt_2_problems": [
        "Custom validation framework from scratch",
        "Abstract validator base class hierarchy",
        "Strategy pattern for different validation types",
        "Observer pattern for validation events",
        "Complex error handling with custom exception types",
        "Validation rule engine with configuration files"
    ],
    "prompt_3_problems": [
        "Complex configuration management system",
        "Abstract factory for environment configs",
        "Singleton pattern for config access",
        "Configuration validation framework",
        "Dynamic configuration reloading system",
        "Custom configuration file format and parser"
    ]
}

# Simple solutions that would actually be appropriate
APPROPRIATE_SOLUTIONS = {
    "prompt_1_simple": """
    // Simple, appropriate solution
    function formatUserName(firstName, lastName) {
      return [firstName, lastName].filter(Boolean).join(' ');
    }
    """,
    "prompt_2_simple": """
    // Simple email validation with formik
    const emailSchema = Yup.string().email('Invalid email').required('Required');
    """,
    "prompt_3_simple": """
    // Simple config object
    const API_ENDPOINTS = {
      dev: 'http://localhost:3000',
      staging: 'https://staging.example.com', 
      production: 'https://api.example.com'
    };
    """
}

def display_over_engineering_analysis():
    """Show how these prompts lead to over-engineering."""
    prompts = [
        ("Example 1: Name Formatting", OVER_ENGINEERED_PROMPT_1),
        ("Example 2: Email Validation", OVER_ENGINEERED_PROMPT_2),
        ("Example 3: API Configuration", OVER_ENGINEERED_PROMPT_3)
    ]
    
    print("=== OVER-ENGINEERING RISK ANALYSIS ===\n")
    
    for i, (title, prompt) in enumerate(prompts, 1):
        print(f"{title}:")
        print("-" * len(title))
        print(prompt.strip())
        
        problem_key = f"prompt_{i}_problems"
        problems = TYPICAL_AI_RESPONSES[problem_key]
        
        print(f"\n🏗️ TYPICAL OVER-ENGINEERED AI RESPONSES:")
        for problem in problems:
            print(f"   • {problem}")
        
        # Show what simple solution would look like
        solution_key = f"prompt_{i}_simple"
        if solution_key in APPROPRIATE_SOLUTIONS:
            print(f"\n✅ APPROPRIATE SIMPLE SOLUTION:")
            print(f"   {APPROPRIATE_SOLUTIONS[solution_key].strip()}")
        
        print("\n" + "="*70 + "\n")

def get_over_engineering_indicators():
    """Return common indicators that a prompt will lead to over-engineering."""
    return {
        "warning_phrases": [
            "enterprise-ready",
            "scalable for future growth", 
            "robust and handle edge cases",
            "good software engineering practices",
            "maintainable and extensible",
            "following design patterns"
        ],
        "missing_constraints": [
            "No complexity limits specified",
            "No examples of appropriate scope shown",
            "No 'keep it simple' guidance",
            "No line count or function count limits",
            "No forbidden design patterns listed"
        ],
        "scope_creep_risks": [
            "Vague requirements allow interpretation",
            "No specific use cases or examples",
            "No current complexity level shown", 
            "No performance or simplicity requirements",
            "Open-ended 'best practices' guidance"
        ]
    }

if __name__ == "__main__":
    display_over_engineering_analysis()
    
    print("=== OVER-ENGINEERING WARNING INDICATORS ===")
    indicators = get_over_engineering_indicators()
    
    for category, items in indicators.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for item in items:
            print(f"  ⚠️ {item}")