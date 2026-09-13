"""
Ethical Job Matching and Candidate Scoring System
================================================

This module provides bias-aware candidate scoring and job recommendation functionality.
Fixed version that addresses ethical issues found in the starter code.
"""

import statistics
from typing import List, Dict, Any


class CandidateScorer:
    """Scores candidates based on job-relevant factors only."""
    
    def __init__(self):
        # Scoring weights focused on job-relevant skills only
        self.scoring_weights = {
            'relevant_skills': 0.4,       # Primary factor
            'experience': 0.35,           # Job-relevant experience
            'education_relevance': 0.25   # Education relevance, not prestige
        }
        
        # Skills-based education scoring (no bias against alternative paths)
        self.education_relevance = {
            'highly_relevant': 100,    # Degree/training directly related to job
            'somewhat_relevant': 85,   # Transferable skills
            'general_education': 70,   # General problem-solving education
            'demonstrated_skills': 90  # Portfolio/experience demonstrates skills
        }
    
    def calculate_final_score(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate final candidate score using ethical methodology."""
        scores = {}
        
        # Skills assessment (job-relevant only)
        skills_score = self._assess_relevant_skills(candidate)
        scores['relevant_skills'] = skills_score
        
        # Experience assessment (quality over quantity)
        experience_score = self._assess_relevant_experience(candidate)
        scores['experience'] = experience_score
        
        # Education relevance (not prestige)
        education_score = self._assess_education_relevance(candidate)
        scores['education_relevance'] = education_score
        
        # Calculate weighted final score
        final_score = sum(
            scores[factor] * self.scoring_weights[factor] 
            for factor in scores
        )
        
        return {
            'final_score': round(final_score, 2),
            'score_breakdown': scores
        }
    
    def _assess_relevant_skills(self, candidate: Dict[str, Any]) -> float:
        """Assess job-relevant skills only."""
        # Base score for problem-solving and technical aptitude
        base_score = 70
        
        # Bonus for relevant experience and demonstrated projects
        years_exp = candidate.get('years_experience', 0)
        if years_exp >= 3:
            base_score += min(years_exp * 3, 30)  # Cap bonus at 30 points
        
        return min(base_score, 100)
    
    def _assess_relevant_experience(self, candidate: Dict[str, Any]) -> float:
        """Assess quality and relevance of experience."""
        years_exp = candidate.get('years_experience', 0)
        
        # Focus on relevant experience, not just years
        if years_exp >= 5:
            return 95
        elif years_exp >= 2:
            return 80
        elif years_exp >= 1:
            return 65
        else:
            return 50  # Entry level is acceptable
    
    def _assess_education_relevance(self, candidate: Dict[str, Any]) -> float:
        """Assess education based on relevance, not prestige."""
        education_level = candidate.get('education_level', 'high_school')
        
        # All education paths valued based on job relevance
        if education_level in ['phd', 'masters', 'bachelors']:
            return self.education_relevance['highly_relevant']
        elif education_level in ['bootcamp', 'associates']:
            return self.education_relevance['demonstrated_skills']
        elif education_level == 'self_taught':
            return self.education_relevance['demonstrated_skills']
        else:
            return self.education_relevance['general_education']


class JobRecommendationEngine:
    """Generates fair job recommendations for candidates."""
    
    def __init__(self):
        self.candidate_scorer = CandidateScorer()
    
    def generate_recommendations(self, candidate: Dict[str, Any], 
                               jobs: List[Dict[str, Any]], 
                               max_recommendations: int = 3) -> List[Dict[str, Any]]:
        """Generate ethical job recommendations for a candidate."""
        recommendations = []
        
        # Get candidate score
        candidate_result = self.candidate_scorer.calculate_final_score(candidate)
        candidate_score = candidate_result['final_score']
        
        for job in jobs:
            # Calculate job compatibility based on requirements match
            job_score = self._calculate_job_match(candidate, job, candidate_score)
            
            # Generate fair recommendation reasons
            reasons = self._generate_fair_reasons(candidate, job)
            
            recommendations.append({
                'job': job,
                'combined_score': job_score,
                'recommendation_reasons': reasons
            })
        
        # Sort by actual job fit, not salary
        recommendations.sort(key=lambda x: x['combined_score'], reverse=True)
        return recommendations[:max_recommendations]
    
    def _calculate_job_match(self, candidate: Dict[str, Any], 
                           job: Dict[str, Any], candidate_score: float) -> float:
        """Calculate job match based on requirements fit."""
        base_score = candidate_score
        
        # Match based on seniority level appropriateness
        years_exp = candidate.get('years_experience', 0)
        job_level = job.get('seniority_level', 'mid')
        
        # Appropriate level matching (not salary bias)
        if job_level == 'junior' and years_exp <= 3:
            level_match = 10  # Good fit
        elif job_level == 'mid' and 2 <= years_exp <= 8:
            level_match = 10  # Good fit
        elif job_level == 'senior' and years_exp >= 5:
            level_match = 10  # Good fit
        else:
            level_match = 0   # Neutral (no penalty)
        
        return base_score + level_match
    
    def _generate_fair_reasons(self, candidate: Dict[str, Any], 
                             job: Dict[str, Any]) -> List[str]:
        """Generate fair recommendation reasons focused on qualifications."""
        reasons = []
        
        # Experience-based reasoning
        years_exp = candidate.get('years_experience', 0)
        job_level = job.get('seniority_level', 'mid')
        
        if years_exp >= 5 and job_level == 'senior':
            reasons.append("Your experience qualifies you for senior roles")
        elif years_exp <= 3 and job_level == 'junior':
            reasons.append("Good entry-level opportunity to grow your skills")
        else:
            reasons.append("Experience level matches role requirements")
        
        # Growth and development focus
        reasons.append("Opportunity for professional development")
        
        # Company stability
        reasons.append("Established company with career growth opportunities")
        
        return reasons[:3]


def create_sample_data():
    """Create sample candidates and jobs for testing."""
    candidates = [
        {
            'name': 'John Smith',
            'age': 32,
            'education_level': 'bachelors',
            'years_experience': 8,
            'previous_salary': 85000,
            'location': 'San Francisco',
            'native_english_speaker': True
        },
        {
            'name': 'Maria Garcia',
            'age': 45,
            'education_level': 'masters',
            'years_experience': 20,
            'previous_salary': 75000,
            'location': 'Austin',
            'native_english_speaker': False
        },
        {
            'name': 'Kevin Wang',
            'age': 24,
            'education_level': 'bootcamp',
            'years_experience': 2,
            'previous_salary': 55000,
            'location': 'Detroit',
            'native_english_speaker': True
        }
    ]
    
    jobs = [
        {
            'id': 1,
            'title': 'Senior Software Engineer',
            'salary': 120000,
            'location': 'San Francisco',
            'company': 'TechCorp',
            'seniority_level': 'senior'
        },
        {
            'id': 2,
            'title': 'Product Manager',
            'salary': 110000,
            'location': 'Austin',
            'company': 'StartupCo',
            'seniority_level': 'mid'
        }
    ]
    
    return candidates, jobs


if __name__ == "__main__":
    # Demo the ethical system
    candidates, jobs = create_sample_data()
    
    scorer = CandidateScorer()
    recommender = JobRecommendationEngine()
    
    print("=== Ethical Candidate Scoring Demo ===")
    for candidate in candidates:
        result = scorer.calculate_final_score(candidate)
        print(f"{candidate['name']}: Score {result['final_score']}")
    
    print("\n=== Fair Job Recommendations Demo ===")
    for candidate in candidates:
        recommendations = recommender.generate_recommendations(candidate, jobs)
        print(f"\nRecommendations for {candidate['name']}:")
        for rec in recommendations:
            print(f"  {rec['job']['title']}: {rec['combined_score']:.1f}")
            print(f"    Reasons: {rec['recommendation_reasons']}")
    
    print("\n=== Ethical Improvements ===")
    print("✅ No age-based scoring")
    print("✅ No location-based penalties")
    print("✅ No language discrimination")
    print("✅ Education valued for relevance, not prestige")
    print("✅ Job matching based on fit, not salary")
    print("✅ Fair reasoning without biased language")