"""
Prompt testing utility to help students evaluate their XML prompt conversions.

This simulates what different AI responses might look like with traditional vs XML prompts.
"""

import re
from typing import Dict, List, Tuple

class PromptAnalyzer:
    """Analyze prompt structure and predict AI response quality."""
    
    def __init__(self):
        self.xml_tags = ['task', 'context', 'requirements', 'constraints']
        self.quality_indicators = {
            'specificity': ['specific', 'exactly', 'must', 'should', 'will'],
            'context': ['existing', 'current', 'architecture', 'system', 'using'],
            'constraints': ['only', 'without', 'cannot', 'forbidden', 'limit'],
            'requirements': ['function', 'method', 'return', 'handle', 'support']
        }
    
    def analyze_traditional_prompt(self, prompt: str) -> Dict[str, any]:
        """Analyze problems in traditional prompt structure."""
        analysis = {
            'structure_score': 0,
            'clarity_score': 0,
            'completeness_score': 0,
            'issues': [],
            'predicted_problems': []
        }
        
        # Check for structural indicators
        sentences = prompt.split('.')
        if len(sentences) == 1:
            analysis['issues'].append("Single run-on sentence - hard to parse")
            analysis['predicted_problems'].append("AI may miss requirements buried in text")
        
        # Check for vague language
        vague_words = ['secure', 'good', 'fast', 'better', 'proper', 'appropriate']
        for word in vague_words:
            if word in prompt.lower():
                analysis['issues'].append(f"Vague term: '{word}' - needs specificity")
                analysis['predicted_problems'].append("AI will guess at specific requirements")
        
        # Check for missing context indicators
        context_indicators = ['existing', 'current', 'our', 'system', 'architecture']
        if not any(indicator in prompt.lower() for indicator in context_indicators):
            analysis['issues'].append("Missing context about existing systems")
            analysis['predicted_problems'].append("AI may propose solutions that don't integrate well")
        
        # Scoring
        analysis['structure_score'] = max(0, 10 - len(analysis['issues']) * 2)
        analysis['clarity_score'] = len([word for word in self.quality_indicators['specificity'] if word in prompt.lower()]) * 2
        analysis['completeness_score'] = len([ind for ind in context_indicators if ind in prompt.lower()]) * 2
        
        return analysis
    
    def analyze_xml_prompt(self, prompt: str) -> Dict[str, any]:
        """Analyze structure and completeness of XML prompt."""
        analysis = {
            'structure_score': 0,
            'clarity_score': 0,
            'completeness_score': 0,
            'strengths': [],
            'improvements_needed': []
        }
        
        # Check for required XML tags
        for tag in self.xml_tags:
            if f'<{tag}>' in prompt and f'</{tag}>' in prompt:
                analysis['structure_score'] += 2.5
                analysis['strengths'].append(f"Proper {tag} structure")
            else:
                analysis['improvements_needed'].append(f"Missing or malformed <{tag}> tags")
        
        # Check for nested structures (advanced)
        if '<functional_requirements>' in prompt or '<performance_requirements>' in prompt:
            analysis['structure_score'] += 2
            analysis['strengths'].append("Advanced nested structure used")
        
        # Check for specific language in requirements
        requirements_section = self.extract_section(prompt, 'requirements')
        if requirements_section:
            specific_words = len([word for word in self.quality_indicators['specificity'] if word in requirements_section.lower()])
            analysis['clarity_score'] = min(10, specific_words * 2)
            if specific_words >= 3:
                analysis['strengths'].append("Requirements use specific, actionable language")
        
        # Check for context completeness
        context_section = self.extract_section(prompt, 'context')
        if context_section:
            context_words = len([word for word in self.quality_indicators['context'] if word in context_section.lower()])
            analysis['completeness_score'] = min(10, context_words * 2)
            if context_words >= 3:
                analysis['strengths'].append("Context provides adequate system information")
        
        return analysis
    
    def extract_section(self, prompt: str, tag: str) -> str:
        """Extract content between XML tags."""
        pattern = f'<{tag}>(.*?)</{tag}>'
        match = re.search(pattern, prompt, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def compare_prompts(self, traditional: str, xml: str) -> Dict[str, any]:
        """Compare traditional vs XML prompt quality."""
        trad_analysis = self.analyze_traditional_prompt(traditional)
        xml_analysis = self.analyze_xml_prompt(xml)
        
        return {
            'traditional': trad_analysis,
            'xml': xml_analysis,
            'improvement': {
                'structure': xml_analysis['structure_score'] - trad_analysis['structure_score'],
                'clarity': xml_analysis['clarity_score'] - trad_analysis['clarity_score'],
                'completeness': xml_analysis['completeness_score'] - trad_analysis['completeness_score']
            }
        }
    
    def display_analysis(self, comparison: Dict[str, any]):
        """Display comparison results in readable format."""
        print("=== PROMPT ANALYSIS COMPARISON ===\n")
        
        print("Traditional Prompt Analysis:")
        print("-" * 30)
        trad = comparison['traditional']
        print(f"Structure Score: {trad['structure_score']}/10")
        print(f"Clarity Score: {trad['clarity_score']}/10")
        print(f"Completeness Score: {trad['completeness_score']}/10")
        
        if trad['issues']:
            print("\nIssues found:")
            for issue in trad['issues']:
                print(f"  ⚠️ {issue}")
        
        if trad['predicted_problems']:
            print("\nPredicted AI problems:")
            for problem in trad['predicted_problems']:
                print(f"  🚨 {problem}")
        
        print("\n" + "="*60)
        
        print("XML Prompt Analysis:")
        print("-" * 20)
        xml = comparison['xml']
        print(f"Structure Score: {xml['structure_score']}/10")
        print(f"Clarity Score: {xml['clarity_score']}/10")
        print(f"Completeness Score: {xml['completeness_score']}/10")
        
        if xml['strengths']:
            print("\nStrengths:")
            for strength in xml['strengths']:
                print(f"  ✅ {strength}")
        
        if xml['improvements_needed']:
            print("\nImprovements needed:")
            for improvement in xml['improvements_needed']:
                print(f"  🔧 {improvement}")
        
        print("\n" + "="*60)
        
        print("Overall Improvement:")
        print("-" * 20)
        imp = comparison['improvement']
        print(f"Structure: +{imp['structure']:.1f} points")
        print(f"Clarity: +{imp['clarity']:.1f} points") 
        print(f"Completeness: +{imp['completeness']:.1f} points")
        
        total_improvement = sum(imp.values())
        print(f"\nTotal Improvement: +{total_improvement:.1f} points")
        
        if total_improvement > 10:
            print("🎉 Excellent improvement! Your XML prompt is much clearer.")
        elif total_improvement > 5:
            print("👍 Good improvement! Keep refining your XML structure.")
        else:
            print("📝 Your XML prompt needs more work. Review the template guidance.")

def test_student_prompts():
    """Interactive function for students to test their prompt conversions."""
    analyzer = PromptAnalyzer()
    
    print("=== PROMPT CONVERSION TESTER ===\n")
    print("This tool helps you compare your traditional and XML prompts.\n")
    
    # You would extend this to load student's actual converted prompts
    # For now, showing the testing framework
    
    sample_traditional = "Write a function to process data from users and make sure it's secure."
    sample_xml = """
<task>
Create a user data processing function with security validation
</task>

<context>
Web application using Flask with PostgreSQL database
Current user data stored in users table with fields: id, email, profile_data
</context>

<requirements>
- Validate all input data before processing
- Sanitize user input to prevent injection attacks
- Return processed data in standardized format
- Log all processing activities for audit
</requirements>

<constraints>
- Use existing database connection pool
- Follow our current logging patterns
- No external validation libraries
- Must handle malformed data gracefully
</constraints>
"""
    
    comparison = analyzer.compare_prompts(sample_traditional, sample_xml)
    analyzer.display_analysis(comparison)

if __name__ == "__main__":
    test_student_prompts()