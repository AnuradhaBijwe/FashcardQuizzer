"""
Tests to verify student XML prompt conversion skills.

These tests check that students have properly structured their XML prompts
and understand the basic concepts from Lesson 3.
"""

import pytest
import re
from typing import List, Dict

class PromptStructureValidator:
    """Validates XML prompt structure and content quality."""
    
    def __init__(self):
        self.required_tags = ['task', 'context', 'requirements', 'constraints']
        self.optional_tags = ['example', 'thinking', 'forbidden_approaches']
    
    def has_proper_xml_structure(self, prompt: str) -> Dict[str, bool]:
        """Check if prompt has proper XML tag structure."""
        results = {}
        for tag in self.required_tags:
            open_tag = f'<{tag}>'
            close_tag = f'</{tag}>'
            results[tag] = open_tag in prompt and close_tag in prompt
        return results
    
    def extract_tag_content(self, prompt: str, tag: str) -> str:
        """Extract content between XML tags."""
        pattern = f'<{tag}>(.*?)</{tag}>'
        match = re.search(pattern, prompt, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def check_content_quality(self, prompt: str) -> Dict[str, List[str]]:
        """Check quality of content within XML tags."""
        issues = []
        strengths = []
        
        # Check task clarity
        task_content = self.extract_tag_content(prompt, 'task')
        if task_content:
            if len(task_content.split()) < 5:
                issues.append("Task description too brief - needs more specificity")
            if any(vague in task_content.lower() for vague in ['good', 'better', 'proper', 'nice']):
                issues.append("Task uses vague language - be more specific")
            else:
                strengths.append("Task description is appropriately detailed")
        
        # Check context completeness
        context_content = self.extract_tag_content(prompt, 'context')
        if context_content:
            context_indicators = ['system', 'architecture', 'existing', 'current', 'database', 'framework']
            found_indicators = [ind for ind in context_indicators if ind in context_content.lower()]
            if len(found_indicators) >= 2:
                strengths.append("Context provides adequate system information")
            else:
                issues.append("Context needs more system/architecture details")
        
        # Check requirements specificity
        req_content = self.extract_tag_content(prompt, 'requirements')
        if req_content:
            # Look for bullet points or list structure
            if '-' in req_content or '•' in req_content or req_content.count('\n') >= 2:
                strengths.append("Requirements are well-structured as list")
            else:
                issues.append("Requirements should be structured as clear list")
            
            # Check for specific verbs
            action_verbs = ['validate', 'process', 'return', 'handle', 'support', 'implement', 'create']
            if any(verb in req_content.lower() for verb in action_verbs):
                strengths.append("Requirements use specific action verbs")
            else:
                issues.append("Requirements need more specific action verbs")
        
        # Check constraints presence
        constraints_content = self.extract_tag_content(prompt, 'constraints')
        if constraints_content:
            constraint_types = ['use', 'no', 'must', 'cannot', 'only', 'without', 'follow']
            if any(ctype in constraints_content.lower() for ctype in constraint_types):
                strengths.append("Constraints specify clear limitations")
            else:
                issues.append("Constraints need clearer limitation language")
        
        return {'issues': issues, 'strengths': strengths}

# Test data - students need to provide their XML conversions
STUDENT_XML_PROMPTS = {
    'data_processing': """
    <!-- STUDENT TODO: Replace this comment with your XML conversion of Traditional Prompt 1 -->
    """,
    'api_caching': """
    <!-- STUDENT TODO: Replace this comment with your XML conversion of Traditional Prompt 2 -->
    """,
    'authentication': """
    <!-- STUDENT TODO: Replace this comment with your XML conversion of Traditional Prompt 3 -->
    """
}

# Sample solutions for testing framework (students don't see this)
SAMPLE_SOLUTIONS = {
    'data_processing': """
<task>
Create a secure user data processing function for form submissions
</task>

<context>
Flask web application with PostgreSQL database
Current user data: registration forms, profile updates, contact submissions
Existing validation uses WTForms with custom validators
</context>

<requirements>
- Validate all input fields against defined schemas
- Sanitize data to prevent XSS and injection attacks  
- Process data into standardized format for database storage
- Return success/error response with validation details
- Log all processing attempts for security audit
</requirements>

<constraints>
- Use existing WTForms validation framework
- Follow current database ORM patterns (SQLAlchemy)
- No external sanitization libraries
- Must maintain backward compatibility with current API
- Response time under 200ms for typical form sizes
</constraints>
""",
    'api_caching': """
<task>
Implement Redis-based caching for high-traffic API endpoints
</task>

<context>
<current_system>
FastAPI application with PostgreSQL database
5 main endpoints serving user data, taking 200-500ms each
Redis instance available but not currently used for API caching
</current_system>

<performance_baseline>
Current response times: 200-500ms average
Target: sub-50ms for cache hits
Expected cache hit rate: 70-80% for read operations
</performance_baseline>
</context>

<requirements>
<functional_requirements>
- Cache GET requests for user profiles, settings, and content
- Implement cache invalidation on data updates
- Handle cache misses gracefully with database fallback
- Support cache TTL configuration per endpoint type
</functional_requirements>

<performance_requirements>
- Reduce median response time to under 50ms for cached responses
- Maintain current performance for cache misses
- Support 1000+ concurrent requests
- Cache hit rate above 70%
</performance_requirements>
</requirements>

<constraints>
- Use existing Redis connection pool
- No changes to current API endpoint signatures
- Must work with existing authentication middleware
- No external caching libraries beyond Redis client
- Preserve all current error handling behavior
</constraints>
""",
    'authentication': """
<task>
Build comprehensive user authentication system with session management
</task>

<context>
<existing_infrastructure>
Node.js/Express application with MongoDB user collection
Current basic login stores plain passwords (needs security upgrade)
User schema: {id, email, password, profile, created_at}
</existing_infrastructure>

<security_requirements>
- bcrypt password hashing (minimum 12 rounds)
- Rate limiting for authentication attempts  
- Session token expiration and refresh
- Input validation for all auth endpoints
</security_requirements>
</context>

<requirements>
<authentication_features>
- User login with email/password validation
- Secure logout with session invalidation
- Password reset via email verification
- Account creation with email confirmation
- Session management with JWT tokens
</authentication_features>

<integration_requirements>
- Work with existing MongoDB user collection
- Integrate with current Express middleware chain
- Support existing frontend authentication flow
- Maintain current user profile structure
</integration_requirements>

<scalability_requirements>
- Handle 1000+ concurrent authentication requests
- Session storage that scales across server instances
- Database query optimization for auth operations
</scalability_requirements>
</requirements>

<constraints>
<forbidden_approaches>
- No external authentication services (Auth0, Firebase, etc.)
- No third-party OAuth providers initially  
- No plain text password storage
- No client-side only validation
</forbidden_approaches>

<technical_constraints>
- Use existing MongoDB connection and user schema
- Work with current Express.js middleware architecture
- No breaking changes to existing user profile endpoints
- Session storage must persist across server restarts
</technical_constraints>
</constraints>
"""
}

class TestPromptStructure:
    """Test cases for XML prompt structure validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = PromptStructureValidator()
    
    @pytest.mark.parametrize("prompt_type", ["data_processing", "api_caching", "authentication"])
    def test_xml_structure_present(self, prompt_type):
        """Test that XML prompts have proper tag structure."""
        prompt = STUDENT_XML_PROMPTS.get(prompt_type, "")
        
        # Skip if student hasn't completed the exercise yet
        if "STUDENT TODO" in prompt or not prompt.strip():
            pytest.skip(f"Student hasn't completed {prompt_type} XML conversion yet")
        
        structure = self.validator.has_proper_xml_structure(prompt)
        
        # All required tags should be present
        missing_tags = [tag for tag, present in structure.items() if not present]
        assert not missing_tags, f"Missing required XML tags: {missing_tags}"
    
    @pytest.mark.parametrize("prompt_type", ["data_processing", "api_caching", "authentication"])
    def test_content_quality(self, prompt_type):
        """Test that XML prompt content meets quality standards."""
        prompt = STUDENT_XML_PROMPTS.get(prompt_type, "")
        
        # Skip if student hasn't completed the exercise yet
        if "STUDENT TODO" in prompt or not prompt.strip():
            pytest.skip(f"Student hasn't completed {prompt_type} XML conversion yet")
        
        quality = self.validator.check_content_quality(prompt)
        
        # Should have more strengths than issues
        assert len(quality['strengths']) >= len(quality['issues']), \
            f"Quality issues found: {quality['issues']}"
        
        # Should have at least 2 quality strengths
        assert len(quality['strengths']) >= 2, \
            f"Prompt needs improvement. Current strengths: {quality['strengths']}"
    
    def test_sample_solution_quality(self):
        """Verify that sample solutions meet all quality standards."""
        for prompt_type, prompt in SAMPLE_SOLUTIONS.items():
            structure = self.validator.has_proper_xml_structure(prompt)
            assert all(structure.values()), f"Sample solution {prompt_type} has structural issues"
            
            quality = self.validator.check_content_quality(prompt)
            assert len(quality['issues']) == 0, f"Sample solution has quality issues: {quality['issues']}"
            assert len(quality['strengths']) >= 3, f"Sample solution lacks sufficient quality indicators"

def test_student_progress():
    """Test to show student progress on XML conversions."""
    completed_prompts = []
    for prompt_type, prompt in STUDENT_XML_PROMPTS.items():
        if "STUDENT TODO" not in prompt and prompt.strip():
            completed_prompts.append(prompt_type)
    
    print(f"\nStudent Progress: {len(completed_prompts)}/3 prompts completed")
    if completed_prompts:
        print(f"Completed: {', '.join(completed_prompts)}")
    
    remaining = set(STUDENT_XML_PROMPTS.keys()) - set(completed_prompts)
    if remaining:
        print(f"Remaining: {', '.join(remaining)}")

if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])