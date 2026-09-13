"""
Tool to test whether XML prompts effectively control complexity and prevent over-engineering.

This analyzer checks if prompts have proper constraints and examples to guide AI toward
appropriately simple solutions.
"""

import re
from typing import Dict, List, Tuple

class ComplexityAnalyzer:
    """Analyze XML prompts for complexity control effectiveness."""
    
    def __init__(self):
        self.complexity_tags = ['complexity_limits', 'forbidden_approaches', 'scope_boundaries', 'simplicity_requirements']
        self.over_engineering_triggers = [
            'enterprise', 'scalable', 'robust', 'extensible', 'maintainable',
            'best practices', 'design patterns', 'architecture', 'framework'
        ]
        self.simplicity_indicators = [
            'simple', 'basic', 'minimal', 'straightforward', 'direct',
            'single', 'one', 'just', 'only'
        ]
    
    def analyze_over_engineering_risk(self, prompt: str) -> Dict[str, any]:
        """Analyze risk of over-engineering in a prompt."""
        analysis = {
            'risk_score': 0,
            'risk_factors': [],
            'protective_factors': [],
            'missing_controls': [],
            'recommendations': []
        }
        
        # Check for over-engineering trigger words
        for trigger in self.over_engineering_triggers:
            if trigger in prompt.lower():
                analysis['risk_score'] += 2
                analysis['risk_factors'].append(f"Contains trigger word: '{trigger}'")
        
        # Check for vague requirements
        if 'good software engineering practices' in prompt.lower():
            analysis['risk_score'] += 3
            analysis['risk_factors'].append("Vague 'good practices' requirement")
        
        if 'handle edge cases' in prompt.lower():
            analysis['risk_score'] += 2
            analysis['risk_factors'].append("Open-ended edge case requirement")
        
        # Check for complexity control measures
        for tag in self.complexity_tags:
            if f'<{tag}>' in prompt:
                analysis['risk_score'] -= 3
                analysis['protective_factors'].append(f"Has {tag} constraints")
            else:
                analysis['missing_controls'].append(f"Missing <{tag}> constraints")
        
        # Check for examples
        if '<example>' in prompt:
            analysis['risk_score'] -= 4
            analysis['protective_factors'].append("Includes complexity-guiding examples")
        else:
            analysis['missing_controls'].append("Missing complexity examples")
        
        # Check for simplicity language
        simplicity_count = sum(1 for indicator in self.simplicity_indicators if indicator in prompt.lower())
        if simplicity_count >= 2:
            analysis['risk_score'] -= 2
            analysis['protective_factors'].append("Uses simplicity language")
        
        # Generate recommendations
        if analysis['risk_score'] > 5:
            analysis['recommendations'].append("HIGH RISK: Add strict complexity limits")
            analysis['recommendations'].append("Add forbidden_approaches to prevent patterns")
            analysis['recommendations'].append("Include simple examples from existing code")
        elif analysis['risk_score'] > 0:
            analysis['recommendations'].append("MEDIUM RISK: Add more complexity constraints")
            analysis['recommendations'].append("Show examples of appropriate simplicity level")
        else:
            analysis['recommendations'].append("LOW RISK: Complexity controls look good")
        
        return analysis
    
    def extract_complexity_controls(self, prompt: str) -> Dict[str, str]:
        """Extract complexity control sections from XML prompt."""
        controls = {}
        
        for tag in self.complexity_tags:
            pattern = f'<{tag}>(.*?)</{tag}>'
            match = re.search(pattern, prompt, re.DOTALL)
            if match:
                controls[tag] = match.group(1).strip()
        
        # Also check for examples
        example_match = re.search(r'<example>(.*?)</example>', prompt, re.DOTALL)
        if example_match:
            controls['example'] = example_match.group(1).strip()
        
        return controls
    
    def evaluate_complexity_controls(self, controls: Dict[str, str]) -> Dict[str, any]:
        """Evaluate effectiveness of complexity control measures."""
        evaluation = {
            'effectiveness_score': 0,
            'strengths': [],
            'weaknesses': [],
            'improvements': []
        }
        
        # Evaluate complexity_limits
        if 'complexity_limits' in controls:
            limits = controls['complexity_limits'].lower()
            if any(word in limits for word in ['lines', 'functions', 'classes', 'files']):
                evaluation['effectiveness_score'] += 3
                evaluation['strengths'].append("Specific size limits defined")
            else:
                evaluation['weaknesses'].append("Complexity limits too vague")
        
        # Evaluate forbidden_approaches
        if 'forbidden_approaches' in controls:
            forbidden = controls['forbidden_approaches'].lower()
            if any(pattern in forbidden for pattern in ['pattern', 'class', 'framework', 'abstract']):
                evaluation['effectiveness_score'] += 3
                evaluation['strengths'].append("Explicitly forbids complex patterns")
            else:
                evaluation['weaknesses'].append("Forbidden approaches not specific enough")
        
        # Evaluate examples
        if 'example' in controls:
            example = controls['example'].lower()
            if len(example.split('\n')) <= 5:  # Simple example
                evaluation['effectiveness_score'] += 2
                evaluation['strengths'].append("Example demonstrates appropriate simplicity")
            else:
                evaluation['weaknesses'].append("Example might be too complex")
        
        # Generate improvement suggestions
        if evaluation['effectiveness_score'] < 5:
            evaluation['improvements'].append("Add more specific complexity limits")
            evaluation['improvements'].append("Include simple code examples")
            evaluation['improvements'].append("Be more explicit about forbidden patterns")
        
        return evaluation
    
    def analyze_prompt_completely(self, prompt: str) -> Dict[str, any]:
        """Complete analysis of prompt for complexity control."""
        risk_analysis = self.analyze_over_engineering_risk(prompt)
        controls = self.extract_complexity_controls(prompt)
        control_evaluation = self.evaluate_complexity_controls(controls)
        
        return {
            'risk_analysis': risk_analysis,
            'extracted_controls': controls,
            'control_effectiveness': control_evaluation,
            'overall_assessment': self._generate_overall_assessment(risk_analysis, control_evaluation)
        }
    
    def _generate_overall_assessment(self, risk_analysis: Dict, control_evaluation: Dict) -> Dict[str, str]:
        """Generate overall assessment of complexity control."""
        risk_score = risk_analysis['risk_score']
        effectiveness_score = control_evaluation['effectiveness_score']
        
        if risk_score <= 0 and effectiveness_score >= 6:
            return {
                'level': 'EXCELLENT',
                'summary': 'Strong complexity controls prevent over-engineering',
                'recommendation': 'Prompt ready for use'
            }
        elif risk_score <= 3 and effectiveness_score >= 4:
            return {
                'level': 'GOOD',
                'summary': 'Adequate complexity controls with minor improvements needed',
                'recommendation': 'Minor refinements recommended'
            }
        elif risk_score <= 6 or effectiveness_score >= 2:
            return {
                'level': 'NEEDS IMPROVEMENT',
                'summary': 'Some complexity controls present but need strengthening',
                'recommendation': 'Add more specific constraints and examples'
            }
        else:
            return {
                'level': 'HIGH RISK',
                'summary': 'Insufficient complexity controls - high over-engineering risk',
                'recommendation': 'Major revision needed with strict complexity limits'
            }

def test_sample_prompts():
    """Test the analyzer with sample prompts."""
    analyzer = ComplexityAnalyzer()
    
    # Sample prompt without complexity controls (high risk)
    risky_prompt = """
    <task>Create a user management system</task>
    <context>Need to manage users in the application</context>
    <requirements>
    - Must be scalable and enterprise-ready
    - Should follow best practices
    - Handle all edge cases robustly
    </requirements>
    <constraints>
    - Should be maintainable and extensible
    </constraints>
    """
    
    # Sample prompt with complexity controls (low risk)
    controlled_prompt = """
    <task>Create a simple user name formatter function</task>
    <context>Need to display user names consistently</context>
    <requirements>
    - Format first and last name for display
    - Handle missing names gracefully
    </requirements>
    <constraints>
    <complexity_limits>
    - Single function, maximum 5 lines
    - No classes or objects
    - Use only built-in string operations
    </complexity_limits>
    <forbidden_approaches>
    - No design patterns
    - No custom frameworks
    - No abstract classes
    </forbidden_approaches>
    </constraints>
    <example>
    // Similar function in our codebase
    function formatEmail(email) {
      return email ? email.toLowerCase() : 'No email';
    }
    </example>
    """
    
    print("=== COMPLEXITY CONTROL ANALYSIS ===\n")
    
    print("HIGH RISK PROMPT ANALYSIS:")
    print("-" * 30)
    analysis1 = analyzer.analyze_prompt_completely(risky_prompt)
    display_analysis_results(analysis1)
    
    print("\n" + "="*60 + "\n")
    
    print("WELL-CONTROLLED PROMPT ANALYSIS:")
    print("-" * 35)
    analysis2 = analyzer.analyze_prompt_completely(controlled_prompt)
    display_analysis_results(analysis2)

def display_analysis_results(analysis: Dict[str, any]):
    """Display analysis results in readable format."""
    risk = analysis['risk_analysis']
    effectiveness = analysis['control_effectiveness']
    overall = analysis['overall_assessment']
    
    print(f"Overall Assessment: {overall['level']}")
    print(f"Summary: {overall['summary']}")
    print(f"Recommendation: {overall['recommendation']}")
    
    print(f"\nRisk Score: {risk['risk_score']} (lower is better)")
    print(f"Effectiveness Score: {effectiveness['effectiveness_score']} (higher is better)")
    
    if risk['risk_factors']:
        print(f"\nRisk Factors:")
        for factor in risk['risk_factors']:
            print(f"  ⚠️ {factor}")
    
    if risk['protective_factors']:
        print(f"\nProtective Factors:")
        for factor in risk['protective_factors']:
            print(f"  ✅ {factor}")
    
    if effectiveness['strengths']:
        print(f"\nStrengths:")
        for strength in effectiveness['strengths']:
            print(f"  💪 {strength}")
    
    if effectiveness['improvements']:
        print(f"\nImprovements Needed:")
        for improvement in effectiveness['improvements']:
            print(f"  🔧 {improvement}")

if __name__ == "__main__":
    test_sample_prompts()