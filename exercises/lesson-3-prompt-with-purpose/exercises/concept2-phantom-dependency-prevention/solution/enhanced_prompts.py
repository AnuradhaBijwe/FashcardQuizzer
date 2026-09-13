"""
Solution: Properly constrained XML prompts that prevent phantom dependencies and over-engineering.
"""

# Solution 1: File processing with comprehensive constraints
ENHANCED_SOLUTION_1 = """
<task>
Optimize file processing performance for large CSV files using chunked reading
</task>

<context>
Python application processing customer data exports
Current implementation reads entire files into memory causing OOM errors
Files range from 100MB to 2GB in size
Performance bottleneck during peak processing times
Current environment: Python 3.9, pandas 1.5.0, standard library modules
</context>

<requirements>
- Reduce memory usage during file processing to under 500MB peak
- Improve processing speed for large files by at least 50%
- Maintain data integrity and existing error handling patterns
- Support concurrent processing of up to 4 files simultaneously
- Preserve existing CSV output format and column structure
</requirements>

<constraints>
<allowed_libraries>
- pandas (version 1.5.0 already installed)
- csv (Python standard library)
- multiprocessing (Python standard library)
- os and sys (Python standard library)
- logging (existing logging configuration)
</allowed_libraries>

<forbidden_approaches>
- No external performance libraries (dask, ray, polars, etc.)
- No libraries not in current requirements.txt
- No distributed computing frameworks
- No custom C extensions or Cython
- No database solutions for temporary storage
- No cloud services or external APIs
</forbidden_approaches>

<complexity_limits>
- Solution should modify existing function, not rewrite entire system
- Maximum 3 new functions, focus on chunked reading approach
- No new classes or complex inheritance hierarchies
- Use existing error handling patterns, don't create new exception types
- Keep solution under 100 lines of new code
</complexity_limits>

<existing_environment>
- Python 3.9 with standard data processing stack
- Existing pandas and csv workflow must be preserved
- Current logging and error handling patterns must be maintained
- No Docker or containerization available
- Limited to single-machine processing
</existing_environment>
</constraints>
"""

# Solution 2: Simple logging with strict scope constraints
ENHANCED_SOLUTION_2 = """
<task>
Add basic logging statements to the discount calculation function
</task>

<context>
E-commerce application with simple pricing logic
Current function: calculate_discount(price, customer_type) returns discount amount
Function is called frequently during checkout process (100+ times per minute)
Existing logging uses Python standard library logger
</context>

<requirements>
- Log function entry with input parameters (price, customer_type)
- Log calculated discount amount before returning
- Use existing logging configuration and format
- Enable debugging of pricing discrepancies
</requirements>

<constraints>
<complexity_limits>
- Maximum 2 logging statements added to existing function
- No new functions, classes, or modules
- No changes to function signature or return behavior
- No logging configuration changes
- Keep function under 15 lines total
</complexity_limits>

<scope_boundaries>
- Only modify the calculate_discount function
- No changes to calling code or error handling
- No new dependencies or imports
- No performance monitoring or metrics collection
- No database logging or external services
</scope_boundaries>

<forbidden_approaches>
- No logging frameworks beyond standard library
- No decorator patterns or aspect-oriented programming
- No abstract base classes or strategy patterns
- No configuration management for logging levels
- No log aggregation or analysis tools
- No complex formatting or structured logging
</forbidden_approaches>

<preservation_requirements>
- Maintain exact function signature: calculate_discount(price, customer_type)
- Preserve all existing business logic and calculations
- Keep existing error handling behavior unchanged
- Maintain current performance characteristics (sub-1ms execution)
- No changes to existing imports or module structure
</preservation_requirements>
</constraints>
"""

# Solution 3: Notification system with platform and integration constraints  
ENHANCED_SOLUTION_3 = """
<task>
Create user notification system for React Native app with Node.js backend
</task>

<context>
React Native mobile application (version 0.70) using Expo managed workflow
Backend API built with Node.js 18 and Express.js 4.18
Current architecture: REST API with JWT authentication, MongoDB database
Currently uses nodemailer for basic email notifications
User management handled by existing /api/users endpoints
</context>

<requirements>
- Send push notifications for critical events (order updates, messages)
- Display in-app notifications with read/unread state management
- Support 3 notification types: info, warning, critical
- Allow users to configure notification preferences per type
- Track notification delivery status and user engagement metrics
</requirements>

<constraints>
<platform_constraints>
- React Native 0.70 with Expo managed workflow limitations
- Node.js 18 with existing Express.js middleware chain
- iOS and Android platform compatibility required
- Expo push notification service (free tier limits: 600k/month)
- MongoDB for persistence, no additional databases
</platform_constraints>

<existing_services>
- Must integrate with current JWT authentication middleware
- Use existing user database schema and /api/users endpoints
- Work with current MongoDB connection and error handling
- Integrate with existing Express.js route structure
- Preserve current API versioning (/api/v1/)
</existing_services>

<forbidden_approaches>
- No external notification services (Firebase, AWS SNS, OneSignal)
- No real-time websocket solutions (Socket.io, WebRTC)
- No message queue systems (Redis, RabbitMQ, Apache Kafka)
- No microservices architecture for notifications
- No third-party analytics platforms
- No complex event-driven architectures
</forbidden_approaches>

<integration_requirements>
- Work with existing user authentication and session management
- Use current MongoDB collections and document structure
- Follow existing API response formatting and error handling
- Integrate with current React Native navigation structure
- Maintain existing app state management patterns (Context API)
- Work within current bundle size limitations (under 50MB)
</integration_requirements>
</constraints>
"""

def display_enhanced_solutions():
    """Display complete enhanced solutions with proper constraints."""
    solutions = [
        ("Enhanced Solution 1: File Processing with Constraints", ENHANCED_SOLUTION_1),
        ("Enhanced Solution 2: Controlled Logging Addition", ENHANCED_SOLUTION_2),
        ("Enhanced Solution 3: Constrained Notification System", ENHANCED_SOLUTION_3)
    ]
    
    print("=== ENHANCED XML SOLUTIONS WITH CONSTRAINTS ===\n")
    
    for title, solution in solutions:
        print(f"{title}:")
        print("=" * len(title))
        print(solution.strip())
        print("\n" + "-"*80 + "\n")

def analyze_constraint_effectiveness():
    """Show how constraints prevent Lesson 2 patterns."""
    effectiveness = {
        "Phantom Dependency Prevention": [
            "allowed_libraries explicitly lists available packages",
            "forbidden_approaches prevents non-existent libraries",
            "existing_environment specifies current setup limitations"
        ],
        "Over-Engineering Prevention": [
            "complexity_limits set clear scope boundaries", 
            "scope_boundaries prevent architectural changes",
            "preservation_requirements maintain existing patterns"
        ],
        "Integration Assurance": [
            "platform_constraints specify technical limitations",
            "existing_services define integration requirements",
            "integration_requirements ensure compatibility"
        ]
    }
    
    print("=== CONSTRAINT EFFECTIVENESS ANALYSIS ===\n")
    
    for category, techniques in effectiveness.items():
        print(f"{category}:")
        print("-" * len(category))
        for technique in techniques:
            print(f"✓ {technique}")
        print()

if __name__ == "__main__":
    display_enhanced_solutions()
    analyze_constraint_effectiveness()