"""
Solution: XML prompts with effective complexity control to prevent over-engineering.

These solutions demonstrate how to use examples, constraints, and scope boundaries
to guide AI toward appropriately simple solutions.
"""

# Solution 1: Name formatting with strict complexity control
COMPLEXITY_SOLUTION_1 = """
<task>
Create a simple function to format user names for display
</task>

<context>
Web application that shows user names in various UI components
Currently concatenating first + last name manually in templates
Need consistent formatting across the application
Current codebase uses simple utility functions for similar tasks
</context>

<requirements>
- Format names as "First Last" for display
- Handle cases where first or last name might be missing
- Return empty string for invalid inputs
- Make it reusable across different components
</requirements>

<constraints>
<complexity_limits>
- Single function, maximum 8 lines of code
- No classes, objects, or complex data structures
- Use only basic JavaScript string operations and array methods
- No configuration systems, external dependencies, or frameworks
- Function should be understandable by junior developers
</complexity_limits>

<forbidden_approaches>
- No design patterns (Strategy, Factory, Builder, Observer, etc.)
- No abstract base classes, inheritance, or OOP architectures
- No custom framework, library, or utility system creation
- No complex validation beyond basic null/undefined checks
- No internationalization systems or locale-specific formatting
- No caching, memoization, or performance optimization systems
</forbidden_approaches>

<scope_boundaries>
- Only create the single formatting function
- No changes to existing templates, components, or calling code
- No new files, modules, or directory structures
- No modifications to build process or configuration
</scope_boundaries>
</constraints>

<example>
Similar simple utility functions in our codebase:
```javascript
// Email formatting utility
function formatEmail(email) {
  return email ? email.toLowerCase().trim() : 'No email provided';
}

// Phone number display utility  
function formatPhone(phone) {
  return phone ? phone.replace(/[^\d]/g, '').slice(-10) : '';
}
```
</example>
"""

# Solution 2: Email validation with scope and complexity boundaries
COMPLEXITY_SOLUTION_2 = """
<task>
Add simple email format validation to user registration form
</task>

<context>
React application with user registration using formik for form handling
Currently accepts any input in email field without validation
Need basic email format validation before form submission
Existing forms use Yup schema validation with simple patterns
</context>

<requirements>
- Validate email format when user submits registration form
- Show clear error message for invalid email formats
- Prevent form submission if email fails validation
- Integration with existing formik validation workflow
</requirements>

<constraints>
<scope_boundaries>
- Only add validation to the existing email field in registration form
- No new validation framework, custom validators, or validation utilities
- No changes to form structure, layout, or other form fields
- Use existing formik + Yup validation patterns already in codebase
- No modifications to form submission or error handling logic
</scope_boundaries>

<complexity_limits>
- Use built-in Yup email validator or simple regex pattern only
- Maximum 3 lines of validation code in schema definition
- No custom validation functions, classes, or complex logic
- No real-time validation, just on-submit validation
- Error message should be single, simple string
</complexity_limits>

<forbidden_approaches>
- No custom validation framework or validation engine creation
- No abstract validator classes, interfaces, or inheritance hierarchies
- No complex validation rules system or configuration management
- No server-side validation API calls during client-side validation
- No advanced email validation (DNS checking, disposable email detection, etc.)
- No validation state management beyond formik's built-in handling
</forbidden_approaches>
</constraints>

<example>
Existing validation patterns in our registration form:
```javascript
const registrationSchema = Yup.object({
  username: Yup.string()
    .required('Username is required')
    .min(3, 'Username too short'),
  password: Yup.string()
    .required('Password is required')
    .min(8, 'Password must be at least 8 characters')
});
```
</example>
"""

# Solution 3: API configuration with simplicity constraints
COMPLEXITY_SOLUTION_3 = """
<task>
Create simple configuration object for API endpoints across environments
</task>

<context>
Node.js application with multiple API endpoints for different services
Currently hardcoding API URLs throughout controllers and service files
Need centralized configuration to support dev, staging, and production environments
Codebase uses simple configuration objects for other settings like cache and database
</context>

<requirements>
- Store all API endpoint URLs in one centralized location
- Support different base URLs for development, staging, and production environments
- Make it easy for developers to add new API endpoints
- Integrate with existing environment variable patterns (NODE_ENV)
</requirements>

<constraints>
<simplicity_requirements>
- Use the simplest solution that solves the immediate problem
- Prefer plain JavaScript objects over complex configuration systems
- Keep configuration easily readable and modifiable by any team member
- No abstractions, patterns, or complexity unless absolutely necessary
- Solution should be obvious to understand without documentation
</simplicity_requirements>

<complexity_limits>
- Single configuration file under 50 lines total
- Plain object structure with no classes, functions, or methods
- No dynamic configuration loading, file parsing, or runtime manipulation
- No validation systems, schema checking, or configuration verification
- No configuration transformation, processing, or manipulation logic
</complexity_limits>

<forbidden_approaches>
- No configuration management frameworks or libraries (dotenv is ok for env vars)
- No dependency injection containers or service locator patterns
- No abstract factory patterns, builders, or configuration object hierarchies
- No complex environment detection systems beyond checking NODE_ENV
- No configuration file parsers for YAML, TOML, or custom formats
- No hot-reloading, dynamic reconfiguration, or runtime config changes
</forbidden_approaches>
</constraints>

<example>
Similar simple configuration objects in our codebase:
```javascript
// Database configuration
const DB_CONFIG = {
  host: process.env.NODE_ENV === 'production' ? 'prod-db.company.com' : 'localhost',
  port: process.env.DB_PORT || 5432,
  database: 'myapp'
};

// Cache settings
const CACHE_SETTINGS = {
  ttl: process.env.NODE_ENV === 'production' ? 3600 : 60,
  maxSize: 1000,
  enabled: process.env.NODE_ENV !== 'test'
};
```
</example>
"""

def display_complexity_solutions():
    """Display complete complexity-controlled solutions."""
    solutions = [
        ("Solution 1: Controlled Name Formatting", COMPLEXITY_SOLUTION_1),
        ("Solution 2: Scoped Email Validation", COMPLEXITY_SOLUTION_2), 
        ("Solution 3: Simple API Configuration", COMPLEXITY_SOLUTION_3)
    ]
    
    print("=== COMPLEXITY-CONTROLLED XML SOLUTIONS ===\n")
    
    for title, solution in solutions:
        print(f"{title}:")
        print("=" * len(title))
        print(solution.strip())
        print("\n" + "-"*80 + "\n")

def analyze_complexity_control_techniques():
    """Analyze the complexity control techniques used in solutions."""
    techniques = {
        "Explicit Size Limits": [
            "Single function, maximum 8 lines of code",
            "Maximum 3 lines of validation code",
            "Single configuration file under 50 lines total"
        ],
        "Forbidden Pattern Prevention": [
            "No design patterns (Strategy, Factory, Builder, etc.)", 
            "No abstract base classes or inheritance",
            "No custom frameworks or complex architectures",
            "No validation engines or configuration management systems"
        ],
        "Scope Boundary Setting": [
            "Only create the single specified function",
            "No changes to existing templates or components",
            "No new files, modules, or directory structures",
            "Focus only on the immediate requirement"
        ],
        "Simplicity Requirements": [
            "Use the simplest solution that works",
            "Prefer built-in language features over libraries", 
            "Keep solution readable by junior developers",
            "No abstractions unless absolutely necessary"
        ],
        "Concrete Examples": [
            "Show similar simple functions from existing codebase",
            "Demonstrate appropriate complexity level",
            "Guide toward consistent patterns and style",
            "Prevent architectural over-engineering"
        ]
    }
    
    print("=== COMPLEXITY CONTROL TECHNIQUES ANALYSIS ===\n")
    
    for technique_type, examples in techniques.items():
        print(f"{technique_type}:")
        print("-" * len(technique_type))
        for example in examples:
            print(f"✓ {example}")
        print()

def demonstrate_effectiveness():
    """Show how these constraints prevent over-engineering patterns."""
    prevention_examples = {
        "Name Formatting Over-Engineering Prevented": [
            "❌ NameFormatter class with multiple methods → ✅ Single 5-line function",
            "❌ Strategy pattern for different formats → ✅ Simple string concatenation", 
            "❌ Abstract base class hierarchy → ✅ Plain JavaScript function",
            "❌ Configuration system for formatting rules → ✅ Hardcoded simple logic"
        ],
        "Email Validation Over-Engineering Prevented": [
            "❌ Custom validation framework → ✅ Built-in Yup email validator",
            "❌ Abstract validator interfaces → ✅ Simple schema definition",
            "❌ Complex validation rule engine → ✅ Single validation line",
            "❌ Real-time validation system → ✅ On-submit validation only"
        ],
        "Configuration Over-Engineering Prevented": [
            "❌ Configuration management framework → ✅ Plain JavaScript object",
            "❌ Abstract factory for configs → ✅ Simple environment checking",
            "❌ Dynamic config loading system → ✅ Static object definition",
            "❌ Configuration validation framework → ✅ Direct property access"
        ]
    }
    
    print("=== OVER-ENGINEERING PREVENTION DEMONSTRATION ===\n")
    
    for category, examples in prevention_examples.items():
        print(f"{category}:")
        print("-" * len(category))
        for example in examples:
            print(f"  {example}")
        print()

if __name__ == "__main__":
    display_complexity_solutions()
    analyze_complexity_control_techniques()
    demonstrate_effectiveness()