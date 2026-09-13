"""
Problematic XML prompts that lack proper constraints.

These prompts demonstrate how missing constraints lead to phantom dependencies
and over-engineering patterns that students learned to recognize in Lesson 2.
"""

# Problem Prompt 1: Missing library constraints - leads to phantom dependencies
PROBLEM_PROMPT_1 = """
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
"""

# Problem Prompt 2: No complexity constraints - leads to over-engineering
PROBLEM_PROMPT_2 = """
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
- Must not impact checkout performance
</constraints>
"""

# Problem Prompt 3: Missing architecture constraints - leads to integration issues
PROBLEM_PROMPT_3 = """
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
- Must work with existing user authentication
- Should not significantly impact app performance
</constraints>
"""

# Problem Analysis: What constraints are missing and what problems this causes
CONSTRAINT_PROBLEMS = {
    "prompt_1": {
        "missing_constraints": [
            "No allowed_libraries specification",
            "No forbidden_approaches list", 
            "No existing_tools context",
            "No external_dependency limitations"
        ],
        "phantom_dependency_risks": [
            "AI might suggest advanced_csv_parser (doesn't exist)",
            "AI might recommend enterprise_file_processor library",
            "AI might propose pandas_accelerator or csv_turbo packages",
            "AI might suggest custom C extensions without build setup"
        ],
        "over_engineering_risks": [
            "Complex distributed processing system for simple file reading",
            "Advanced caching layers when simple chunking would work",
            "Microservices architecture for file processing",
            "Complex queue systems for straightforward batch processing"
        ]
    },
    "prompt_2": {
        "missing_constraints": [
            "No complexity_limits specified",
            "No pattern restrictions",
            "No scope boundaries", 
            "No existing_code preservation requirements"
        ],
        "phantom_dependency_risks": [
            "AI might suggest advanced_logging_framework",
            "AI might recommend log_aggregator packages",
            "AI might propose custom logging decorators requiring new dependencies"
        ],
        "over_engineering_risks": [
            "Complex logging architecture with multiple handlers",
            "Advanced log correlation and tracing systems", 
            "Strategy pattern implementations for simple logging",
            "Abstract base classes and complex inheritance hierarchies",
            "Configuration management systems for basic logging"
        ]
    },
    "prompt_3": {
        "missing_constraints": [
            "No platform_specific limitations",
            "No existing_service_integration requirements",
            "No deployment_constraints specified",
            "No external_service restrictions"
        ],
        "phantom_dependency_risks": [
            "AI might suggest notification_master library",
            "AI might recommend push_notification_pro package",
            "AI might propose custom notification gateways",
            "AI might suggest enterprise notification platforms"
        ],
        "over_engineering_risks": [
            "Complex event-driven architecture for simple notifications",
            "Advanced message queuing systems like Apache Kafka",
            "Microservices for notification delivery",
            "Complex state machines for notification workflows",
            "Advanced analytics and ML-based notification optimization"
        ]
    }
}

def display_problem_analysis():
    """Display problematic prompts and their constraint issues."""
    prompts = [
        ("Problem 1: File Processing Optimization", PROBLEM_PROMPT_1),
        ("Problem 2: Simple Logging Addition", PROBLEM_PROMPT_2),
        ("Problem 3: Notification System", PROBLEM_PROMPT_3)
    ]
    
    print("=== PROBLEMATIC PROMPTS ANALYSIS ===\n")
    
    for i, (title, prompt) in enumerate(prompts, 1):
        print(f"{title}:")
        print("-" * len(title))
        print(prompt.strip())
        
        problem_key = f"prompt_{i}"
        problems = CONSTRAINT_PROBLEMS[problem_key]
        
        print(f"\n🚨 MISSING CONSTRAINTS:")
        for constraint in problems["missing_constraints"]:
            print(f"   • {constraint}")
        
        print(f"\n👻 PHANTOM DEPENDENCY RISKS:")
        for risk in problems["phantom_dependency_risks"]:
            print(f"   • {risk}")
            
        print(f"\n🏗️  OVER-ENGINEERING RISKS:")
        for risk in problems["over_engineering_risks"]:
            print(f"   • {risk}")
        
        print("\n" + "="*80 + "\n")

def get_constraint_improvement_checklist():
    """Return checklist for improving each problematic prompt."""
    return {
        "prompt_1": [
            "Add <allowed_libraries> tag with standard library and existing packages",
            "Include <forbidden_approaches> to prevent complex distributed solutions", 
            "Specify <complexity_limits> for appropriate solution scope",
            "Add <existing_tools> context about current Python environment"
        ],
        "prompt_2": [
            "Add <complexity_limits> to prevent over-engineering simple logging",
            "Include <forbidden_approaches> to prevent design patterns for simple tasks",
            "Specify <scope_boundaries> to limit changes to logging addition only",
            "Add <preservation_requirements> to maintain existing function structure"
        ],
        "prompt_3": [
            "Add <platform_constraints> for React Native and Node.js limitations",
            "Include <existing_services> context about current infrastructure",
            "Specify <forbidden_approaches> to prevent complex messaging architectures",
            "Add <integration_requirements> for working with current auth and API"
        ]
    }

if __name__ == "__main__":
    display_problem_analysis()
    
    print("=== CONSTRAINT IMPROVEMENT CHECKLIST ===")
    checklist = get_constraint_improvement_checklist()
    for prompt, improvements in checklist.items():
        print(f"\n{prompt.replace('_', ' ').title()} Improvements:")
        for improvement in improvements:
            print(f"  ☐ {improvement}")