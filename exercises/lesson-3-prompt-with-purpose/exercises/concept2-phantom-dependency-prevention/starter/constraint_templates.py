"""
Templates for adding proper constraints to XML prompts.
Students will use these to enhance the problematic prompts.
"""

# Template 1: File processing with library and complexity constraints
CONSTRAINT_TEMPLATE_1 = """
<task>
Optimize file processing performance for large CSV files
</task>

<context>
Python application processing customer data exports
Current implementation reads entire files into memory
Files range from 100MB to 2GB in size
Performance bottleneck during peak processing times
</context>

<requirements>
- Reduce memory usage during file processing
- Improve processing speed for large files
- Maintain data integrity and error handling
- Support concurrent file processing
</requirements>

<constraints>
<allowed_libraries>
[STUDENT TODO: List available libraries - pandas, csv, multiprocessing, etc.]
</allowed_libraries>

<forbidden_approaches>
[STUDENT TODO: Prevent phantom dependencies and over-engineering]
</forbidden_approaches>

<complexity_limits>
[STUDENT TODO: Set appropriate solution scope boundaries]
</complexity_limits>

<existing_environment>
[STUDENT TODO: Specify current Python setup and limitations]
</existing_environment>
</constraints>
"""

# Template 2: Simple logging with scope constraints  
CONSTRAINT_TEMPLATE_2 = """
<task>
Add logging to the discount calculation function
</task>

<context>
E-commerce application with simple pricing logic
Current function calculates customer discounts based on tier
Function is called frequently during checkout process
</context>

<requirements>
- Log when discount calculations occur
- Track discount amounts applied
- Enable debugging of pricing issues
</requirements>

<constraints>
<complexity_limits>
[STUDENT TODO: Prevent over-engineering for simple logging]
</complexity_limits>

<scope_boundaries>
[STUDENT TODO: Limit changes to logging addition only]
</scope_boundaries>

<forbidden_approaches>
[STUDENT TODO: Prevent design patterns and complex architectures]
</forbidden_approaches>

<preservation_requirements>
[STUDENT TODO: Maintain existing function structure]
</preservation_requirements>
</constraints>
"""

# Template 3: Notification system with platform constraints
CONSTRAINT_TEMPLATE_3 = """
<task>
Create user notification system for the mobile app
</task>

<context>
React Native mobile application
Backend API built with Node.js and Express
Currently uses basic email notifications
Need to add push notifications and in-app messages
</context>

<requirements>
- Send push notifications for important events
- Display in-app notifications for user actions
- Support different notification types and priorities
- Allow users to configure notification preferences
- Track notification delivery and engagement
</requirements>

<constraints>
<platform_constraints>
[STUDENT TODO: React Native and Node.js specific limitations]
</platform_constraints>

<existing_services>
[STUDENT TODO: Current infrastructure to integrate with]
</existing_services>

<forbidden_approaches>
[STUDENT TODO: Prevent complex messaging architectures]
</forbidden_approaches>

<integration_requirements>
[STUDENT TODO: Work with current auth and API structure]
</integration_requirements>
</constraints>
"""

CONSTRAINT_GUIDANCE = {
    "allowed_libraries": {
        "purpose": "Explicitly list available dependencies to prevent phantom libraries",
        "examples": ["pandas (already installed)", "csv (standard library)", "multiprocessing (standard library)"],
        "pattern_prevention": "Eliminates phantom dependency pattern from Lesson 2"
    },
    "forbidden_approaches": {
        "purpose": "Prevent over-engineering and inappropriate solutions", 
        "examples": ["No microservices for simple tasks", "No external libraries not in requirements.txt", "No complex design patterns for simple functions"],
        "pattern_prevention": "Eliminates over-engineering pattern from Lesson 2"
    },
    "complexity_limits": {
        "purpose": "Set boundaries on solution scope and complexity",
        "examples": ["Maximum 20 lines of new code", "Single file modification only", "No new classes or abstractions"],
        "pattern_prevention": "Controls solution scope to prevent over-engineering"
    }
}

def display_constraint_templates():
    """Show constraint templates with guidance."""
    templates = [
        ("Template 1: File Processing Constraints", CONSTRAINT_TEMPLATE_1),
        ("Template 2: Simple Logging Constraints", CONSTRAINT_TEMPLATE_2),
        ("Template 3: Notification System Constraints", CONSTRAINT_TEMPLATE_3)
    ]
    
    print("=== CONSTRAINT ENHANCEMENT TEMPLATES ===\n")
    
    for title, template in templates:
        print(f"{title}:")
        print("-" * len(title))
        print(template.strip())
        print("\n" + "="*70 + "\n")

def display_constraint_guidance():
    """Show guidance for different constraint types."""
    print("=== CONSTRAINT TYPE GUIDANCE ===\n")
    
    for constraint_type, guidance in CONSTRAINT_GUIDANCE.items():
        print(f"{constraint_type.replace('_', ' ').title()}:")
        print(f"  Purpose: {guidance['purpose']}")
        print(f"  Examples: {', '.join(guidance['examples'])}")
        print(f"  Pattern Prevention: {guidance['pattern_prevention']}")
        print()

if __name__ == "__main__":
    display_constraint_templates()
    display_constraint_guidance()