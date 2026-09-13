"""
Solution: Structured conversions of traditional prompts demonstrating proper organization.

These solutions show how to effectively convert vague traditional prompts 
into clear, structured format using Lesson 3 techniques. We use XML as our example 
format, but the same principles apply to any structured approach.
"""

# Solution 1: Data processing prompt with proper structured format
XML_SOLUTION_1 = """
<task>
Create a secure user data processing function for form submissions
</task>

<context>
Flask web application with PostgreSQL database
Current user data: registration forms, profile updates, contact submissions
Existing validation uses WTForms with custom validators
Current architecture uses SQLAlchemy ORM for database operations
</context>

<requirements>
- Validate all input fields against defined schemas
- Sanitize data to prevent XSS and injection attacks  
- Process data into standardized format for database storage
- Return success/error response with validation details
- Log all processing attempts for security audit
- Handle edge cases like malformed JSON and oversized payloads
</requirements>

<constraints>
- Use existing WTForms validation framework
- Follow current database ORM patterns (SQLAlchemy)
- No external sanitization libraries beyond existing stack
- Must maintain backward compatibility with current API
- Response time under 200ms for typical form sizes
- Follow existing logging patterns for consistency
</constraints>
"""

# Solution 2: API caching prompt with nested XML structure
XML_SOLUTION_2 = """
<task>
Implement Redis-based caching for high-traffic API endpoints
</task>

<context>
<current_system>
FastAPI application with PostgreSQL database
5 main endpoints serving user data: /users/{id}, /profiles/{id}, /settings/{id}, /content/{id}, /analytics/{id}
Current response times: 200-500ms average per endpoint
Redis instance available at redis://localhost:6379 but not used for API caching
</current_system>

<performance_baseline>
Current median response time: 300ms
95th percentile: 800ms
Target: sub-50ms for cache hits, maintain <300ms for cache misses
Expected cache hit rate: 70-80% for read operations
</performance_baseline>
</context>

<requirements>
<functional_requirements>
- Cache GET requests for user profiles, settings, and content endpoints
- Implement automatic cache invalidation on data updates (POST, PUT, DELETE)
- Handle cache misses gracefully with database fallback
- Support configurable TTL per endpoint type (profiles: 5min, settings: 15min, content: 1hour)
- Implement cache warming for frequently accessed data
</functional_requirements>

<performance_requirements>
- Reduce median response time to under 50ms for cached responses
- Maintain current performance levels for cache misses
- Support 1000+ concurrent requests without degradation
- Achieve cache hit rate above 70% within 24 hours of deployment
- Memory usage for cache under 1GB
</performance_requirements>
</requirements>

<constraints>
- Use existing Redis connection pool configuration
- No changes to current API endpoint signatures or authentication
- Must work with existing rate limiting and authentication middleware
- No external caching libraries beyond redis-py
- Preserve all current error handling and logging behavior
- Cache keys must prevent collisions across different tenants
</constraints>
"""

# Solution 3: Authentication system with comprehensive XML structure
XML_SOLUTION_3 = """
<task>
Build comprehensive user authentication system with session management
</task>

<context>
<existing_infrastructure>
Node.js/Express application with MongoDB user collection
Current basic login stores plain passwords (critical security issue to fix)
User schema: {_id, email, password, profile, created_at, last_login}
Express middleware chain includes cors, helmet, body parser
Frontend: React SPA expecting JWT token authentication
</existing_infrastructure>

<security_requirements>
- bcrypt password hashing with minimum 12 salt rounds
- Rate limiting: 5 attempts per IP per minute for auth endpoints
- JWT tokens with 30-minute expiration and refresh capability
- Input validation and sanitization for all auth endpoints
- HTTPS enforcement for all authentication operations
</security_requirements>
</context>

<requirements>
<authentication_features>
- User login with email/password validation and secure session creation
- Secure logout with JWT token invalidation and session cleanup
- Password reset via email verification with time-limited tokens
- Account creation with email confirmation before activation
- JWT token refresh mechanism for seamless user experience
- Account lockout after repeated failed login attempts
</authentication_features>

<integration_requirements>
- Work with existing MongoDB user collection and schema
- Integrate seamlessly with current Express middleware chain
- Support existing React frontend authentication flow and state management
- Maintain current user profile structure and API endpoints
- Work with existing email service for password resets
</integration_requirements>

<scalability_requirements>
- Handle 1000+ concurrent authentication requests
- JWT token validation that scales across multiple server instances
- Database query optimization for auth operations (indexed lookups)
- Session storage that persists across server restarts
- Efficient cleanup of expired tokens and reset codes
</scalability_requirements>
</requirements>

<constraints>
<forbidden_approaches>
- No external authentication services (Auth0, Firebase Auth, Okta)
- No third-party OAuth providers in initial implementation
- No plain text password storage anywhere in system
- No client-side only validation (all validation must be server-side)
- No session data in local storage (security risk)
</forbidden_approaches>

<technical_constraints>
- Use existing MongoDB connection and user collection schema
- Work within current Express.js middleware architecture
- No breaking changes to existing user profile or settings endpoints
- JWT secret must be environment variable, not hardcoded
- Session storage must handle horizontal scaling (multiple server instances)
- Password reset tokens expire within 1 hour for security
</technical_constraints>
</constraints>
"""

def display_solutions():
    """Display complete XML solution prompts."""
    solutions = [
        ("XML Solution 1: Secure Data Processing", XML_SOLUTION_1),
        ("XML Solution 2: Redis API Caching", XML_SOLUTION_2),
        ("XML Solution 3: Complete Authentication System", XML_SOLUTION_3)
    ]
    
    print("=== COMPLETE XML PROMPT SOLUTIONS ===\n")
    
    for title, solution in solutions:
        print(f"{title}:")
        print("=" * len(title))
        print(solution.strip())
        print("\n" + "-"*80 + "\n")

def analyze_solution_improvements():
    """Show how XML structure improves upon traditional prompts."""
    improvements = {
        "Solution 1": [
            "Task clearly specifies 'secure user data processing' instead of vague 'process data'",
            "Context explains exact system architecture (Flask, PostgreSQL, WTForms)",
            "Requirements break down security, functionality, and performance needs separately",
            "Constraints specify exact frameworks and compatibility requirements"
        ],
        "Solution 2": [
            "Task specifies exact caching technology and scope",
            "Context uses nested structure to separate system info from performance baseline",
            "Requirements separate functional from performance concerns with specific metrics",
            "Constraints prevent integration problems and specify technical limitations"
        ],
        "Solution 3": [
            "Task breaks down complex system into specific, manageable objective", 
            "Context separates infrastructure, security, and integration concerns",
            "Requirements use three-tier structure: features, integration, scalability",
            "Constraints clearly separate forbidden approaches from technical limitations"
        ]
    }
    
    print("=== KEY IMPROVEMENTS ANALYSIS ===\n")
    
    for solution, improvement_list in improvements.items():
        print(f"{solution} Improvements:")
        print("-" * (len(solution) + 15))
        for improvement in improvement_list:
            print(f"✓ {improvement}")
        print()

if __name__ == "__main__":
    display_solutions()
    analyze_solution_improvements()