"""
Tests to verify student complexity control skills.

These tests check that students can create XML prompts that prevent over-engineering
through appropriate constraints and examples.
"""

import pytest
import re
from typing import List, Dict

# Student XML prompts - to be completed by students
STUDENT_PROMPTS = {
    'name_formatting': """
    <!-- STUDENT TODO: Replace this comment with your complexity-controlled XML prompt for name formatting -->
    """,
    'email_validation': """
    <!-- STUDENT TODO: Replace this comment with your complexity-controlled XML prompt for email validation -->
    """,
    'api_configuration': """
    <!-- STUDENT TODO: Replace this comment with your complexity-controlled XML prompt for API configuration -->
    """
}

# Sample solutions for testing framework
SAMPLE_SOLUTIONS = {
    'name_formatting': """
<task>
Create a simple function to format user names for display
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
- Single function, maximum 8 lines
- No classes, objects, or complex data structures
- Use only basic string operations
- No configuration systems or external dependencies
</complexity_limits>

<forbidden_approaches>
- No design patterns (Strategy, Factory, Builder, etc.)
- No abstract base classes or inheritance
- No custom framework or library creation
- No complex validation or error handling beyond basic checks
</forbidden_approaches>

<scope_boundaries>
- Only create the formatting function
- No changes to existing templates or components
- No new files or modules
</scope_boundaries>
</constraints>

<example>
Similar simple utility in our codebase:
```javascript
function formatEmail(email) {
  return email ? email.toLowerCase().trim() : 'No email provided';
}
```
</example>
""",
    'email_validation': """
<task>
Add simple email format validation to user registration form
</task>

<context>
React application with user registration using formik
Currently accepts any input in email field
Need to validate email format before submission
</context>

<requirements>
- Validate email format on form submission
- Show error message for invalid emails  
- Prevent form submission if email is invalid
</requirements>

<constraints>
<scope_boundaries>
- Only add validation to existing email field
- No new validation framework or custom validators
- No changes to form structure or other fields
- Use existing formik validation patterns
</scope_boundaries>

<complexity_limits>
- Use built-in or simple regex validation only
- Maximum 3 lines of validation code
- No custom validation classes or functions
- No complex error handling beyond basic message display
</complexity_limits>

<forbidden_approaches>
- No custom validation framework creation
- No abstract validator classes
- No complex validation rules engine
- No real-time validation servers or APIs
</forbidden_approaches>
</constraints>

<example>
Existing validation pattern in our forms:
```javascript
const schema = Yup.object({
  username: Yup.string().required('Username is required'),
  password: Yup.string().min(8, 'Password too short')
});
```
</example>
""",
    'api_configuration': """
<task>
Create simple configuration object for API endpoints
</task>

<context>
Node.js application with multiple API endpoints
Currently hardcoding URLs throughout the codebase
Need centralized configuration for different environments
</context>

<requirements>
- Store API URLs in one centralized place
- Support different URLs for dev/staging/production
- Make it easy to add new endpoints
</requirements>

<constraints>
<simplicity_requirements>
- Use the simplest solution that works
- Prefer plain JavaScript objects over complex systems
- Keep configuration readable by any developer
- No abstractions unless absolutely necessary
</simplicity_requirements>

<complexity_limits>
- Single configuration file, under 50 lines
- Plain object structure, no classes
- No dynamic configuration loading or management
- No validation or transformation systems
</complexity_limits>

<forbidden_approaches>
- No configuration management frameworks
- No dependency injection containers
- No abstract factory patterns for config
- No complex environment detection systems
- No configuration file parsers or custom formats
</forbidden_approaches>
</constraints>

<example>
Similar simple config in our codebase:
```javascript
const CACHE_SETTINGS = {
  ttl: process.env.NODE_ENV === 'production' ? 3600 : 60,
  maxSize: 1000
};
```
</example>
"""
}

class ComplexityControlValidator:
    """Validates complexity control in XML prompts."""
    
    def __init__(self):
        self.required_complexity_tags = ['complexity_limits', 'forbidden_approaches']
        self.optional_complexity_tags = ['scope_boundaries', 'simplicity_requirements']
        self.over_engineering_triggers = [
            'enterprise', 'scalable', 'robust', 'extensible', 'architecture',
            'best practices', 'design patterns', 'framework'
        ]
    
    def has_complexity_controls(self, prompt: str) -> Dict[str, bool]:
        """Check if prompt has proper complexity control tags."""
        results = {}
        all_tags = self.required_complexity_tags + self.optional_complexity_tags
        
        for tag in all_tags:
            open_tag = f'<{tag}>'
            close_tag = f'</{tag}>'
            results[tag] = open_tag in prompt and close_tag in prompt
        
        return results
    
    def check_over_engineering_risks(self, prompt: str) -> List[str]:
        """Check for language that might trigger over-engineering."""
        risks = []
        
        # Remove all constraint sections from risk analysis (they're protective, not risky)
        constraint_patterns = [
            r'<constraints>.*?</constraints>',
            r'<forbidden_approaches>.*?</forbidden_approaches>',
            r'<complexity_limits>.*?</complexity_limits>',
            r'<scope_boundaries>.*?</scope_boundaries>',
            r'<simplicity_requirements>.*?</simplicity_requirements>'
        ]
        
        prompt_without_constraints = prompt
        for pattern in constraint_patterns:
            prompt_without_constraints = re.sub(pattern, '', prompt_without_constraints, flags=re.DOTALL)
        
        for trigger in self.over_engineering_triggers:
            if trigger in prompt_without_constraints.lower():
                risks.append(f"Contains over-engineering trigger: '{trigger}'")
        
        # Check for vague requirements in main prompt (not in constraints)
        if 'handle edge cases' in prompt_without_constraints.lower():
            risks.append("Vague 'handle edge cases' requirement")
        
        if 'good software engineering practices' in prompt_without_constraints.lower():
            risks.append("Vague 'good practices' requirement")
        
        return risks
    
    def extract_tag_content(self, prompt: str, tag: str) -> str:
        """Extract content between XML tags."""
        pattern = f'<{tag}>(.*?)</{tag}>'
        match = re.search(pattern, prompt, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def evaluate_constraints_quality(self, prompt: str) -> Dict[str, List[str]]:
        """Evaluate quality of complexity constraints."""
        evaluation = {'strengths': [], 'weaknesses': []}
        
        # Check complexity_limits content
        limits_content = self.extract_tag_content(prompt, 'complexity_limits')
        if limits_content:
            if any(word in limits_content.lower() for word in ['lines', 'functions', 'single', 'maximum']):
                evaluation['strengths'].append("Complexity limits are specific and measurable")
            else:
                evaluation['weaknesses'].append("Complexity limits too vague")
        
        # Check forbidden_approaches content
        forbidden_content = self.extract_tag_content(prompt, 'forbidden_approaches')
        if forbidden_content:
            if any(pattern in forbidden_content.lower() for pattern in ['pattern', 'class', 'framework', 'abstract']):
                evaluation['strengths'].append("Forbidden approaches prevent complex patterns")
            else:
                evaluation['weaknesses'].append("Forbidden approaches not specific enough")
        
        # Check for examples
        example_content = self.extract_tag_content(prompt, 'example')
        if example_content:
            if len(example_content.split('\n')) <= 10:  # Simple example
                evaluation['strengths'].append("Example demonstrates appropriate simplicity")
            else:
                evaluation['weaknesses'].append("Example might be too complex")
        
        return evaluation

class TestComplexityControl:
    """Test cases for complexity control validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = ComplexityControlValidator()
    
    @pytest.mark.parametrize("prompt_type", ["name_formatting", "email_validation", "api_configuration"])
    def test_has_complexity_controls(self, prompt_type):
        """Test that prompts have proper complexity control tags."""
        prompt = STUDENT_PROMPTS.get(prompt_type, "")
        
        # Skip if student hasn't completed the exercise yet
        if "STUDENT TODO" in prompt or not prompt.strip():
            pytest.skip(f"Student hasn't completed {prompt_type} complexity control yet")
        
        controls = self.validator.has_complexity_controls(prompt)
        
        # Must have at least one required complexity control tag
        required_present = any(controls.get(tag, False) for tag in self.validator.required_complexity_tags)
        assert required_present, f"Missing required complexity control tags: {self.validator.required_complexity_tags}"
    
    @pytest.mark.parametrize("prompt_type", ["name_formatting", "email_validation", "api_configuration"])
    def test_over_engineering_prevention(self, prompt_type):
        """Test that prompts prevent over-engineering patterns."""
        prompt = STUDENT_PROMPTS.get(prompt_type, "")
        
        # Skip if student hasn't completed the exercise yet
        if "STUDENT TODO" in prompt or not prompt.strip():
            pytest.skip(f"Student hasn't completed {prompt_type} complexity control yet")
        
        risks = self.validator.check_over_engineering_risks(prompt)
        
        # Should have minimal over-engineering risk factors
        assert len(risks) <= 1, f"Too many over-engineering risks: {risks}"
    
    @pytest.mark.parametrize("prompt_type", ["name_formatting", "email_validation", "api_configuration"])
    def test_constraint_quality(self, prompt_type):
        """Test that complexity constraints are well-designed."""
        prompt = STUDENT_PROMPTS.get(prompt_type, "")
        
        # Skip if student hasn't completed the exercise yet
        if "STUDENT TODO" in prompt or not prompt.strip():
            pytest.skip(f"Student hasn't completed {prompt_type} complexity control yet")
        
        evaluation = self.validator.evaluate_constraints_quality(prompt)
        
        # Should have more strengths than weaknesses
        assert len(evaluation['strengths']) >= len(evaluation['weaknesses']), \
            f"Constraint quality issues: {evaluation['weaknesses']}"
        
        # Should have at least one strength
        assert len(evaluation['strengths']) >= 1, \
            "Complexity constraints need improvement"
    
    def test_sample_solution_quality(self):
        """Verify that sample solutions meet all complexity control standards."""
        for prompt_type, prompt in SAMPLE_SOLUTIONS.items():
            controls = self.validator.has_complexity_controls(prompt)
            assert any(controls.values()), f"Sample solution {prompt_type} lacks complexity controls"
            
            risks = self.validator.check_over_engineering_risks(prompt)
            assert len(risks) == 0, f"Sample solution has over-engineering risks: {risks}"
            
            evaluation = self.validator.evaluate_constraints_quality(prompt)
            assert len(evaluation['weaknesses']) == 0, f"Sample solution has constraint issues: {evaluation['weaknesses']}"
            assert len(evaluation['strengths']) >= 2, f"Sample solution lacks sufficient quality indicators"

def test_student_progress():
    """Test to show student progress on complexity control."""
    completed_prompts = []
    for prompt_type, prompt in STUDENT_PROMPTS.items():
        if "STUDENT TODO" not in prompt and prompt.strip():
            completed_prompts.append(prompt_type)
    
    print(f"\nStudent Progress: {len(completed_prompts)}/3 complexity control prompts completed")
    if completed_prompts:
        print(f"Completed: {', '.join(completed_prompts)}")
    
    remaining = set(STUDENT_PROMPTS.keys()) - set(completed_prompts)
    if remaining:
        print(f"Remaining: {', '.join(remaining)}")

def test_complexity_analysis_demo():
    """Demonstrate complexity analysis on sample prompts."""
    from simplicity_tester import ComplexityAnalyzer
    
    analyzer = ComplexityAnalyzer()
    
    print("\n=== COMPLEXITY ANALYSIS DEMONSTRATION ===")
    
    # Test one of the sample solutions
    sample_prompt = SAMPLE_SOLUTIONS['name_formatting']
    analysis = analyzer.analyze_prompt_completely(sample_prompt)
    
    overall = analysis['overall_assessment']
    print(f"\nSample Solution Analysis:")
    print(f"Level: {overall['level']}")
    print(f"Summary: {overall['summary']}")
    
    if analysis['control_effectiveness']['strengths']:
        print("Strengths:")
        for strength in analysis['control_effectiveness']['strengths']:
            print(f"  ✅ {strength}")

if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])