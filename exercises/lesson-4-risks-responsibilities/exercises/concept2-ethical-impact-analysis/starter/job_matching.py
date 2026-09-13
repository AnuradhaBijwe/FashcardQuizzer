"""
AI-Generated Job Matching and Candidate Scoring System
=====================================================

This module provides candidate scoring and job recommendation functionality.
Generated to help match candidates with suitable job opportunities.
"""

import statistics
from typing import List, Dict, Any


class CandidateScorer:
    """Scores candidates based on various factors."""
    
    def __init__(self):
        # Scoring weights for different factors
        self.scoring_weights = {
            'education': 0.3,
            'experience': 0.25,
            'age_factor': 0.2,        # Age-based scoring
            'location': 0.15,
            'communication': 0.1
        }
        
        # Education level scoring
        self.education_scores = {
            'phd': 100,
            'masters': 85,
            'bachelors': 70,
            'associates': 50,
            'high_school': 35,
            'bootcamp': 40,           # Lower than traditional degrees
            'self_taught': 30         # Lowest score
        }
        
        # Location premium scoring
        self.location_multipliers = {
            'San Francisco': 1.2,     # Premium for expensive cities
            'New York': 1.15,
            'Austin': 1.0,
            'Detroit': 0.85,          # Penalty for less prestigious locations
            'rural_areas': 0.7        # Significant penalty
        }
    
    def calculate_final_score(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate final candidate score."""
        scores = {}
        
        # Education score
        education_level = candidate.get('education_level', 'high_school')
        education_score = self.education_scores.get(education_level, 35)
        scores['education'] = education_score
        
        # Experience score
        years_exp = candidate.get('years_experience', 0)
        experience_score = min(years_exp * 10, 100)  # Cap at 100
        scores['experience'] = experience_score
        
        # Age factor - discriminatory scoring
        age = candidate.get('age', 25)
        if age < 25:
            age_score = 60  # Too young
        elif 25 <= age <= 35:
            age_score = 100  # Ideal age range
        elif 36 <= age <= 45:
            age_score = 80   # Getting older
        else:
            age_score = 50   # Too old - age discrimination
        scores['age_factor'] = age_score
        
        # Location scoring - geographic bias
        location = candidate.get('location', 'rural_areas')
        location_multiplier = self.location_multipliers.get(location, 0.8)
        location_score = 70 * location_multiplier
        scores['location'] = location_score
        
        # Communication score - biased against non-native speakers
        is_native_speaker = candidate.get('native_english_speaker', True)
        if is_native_speaker:
            communication_score = 90
        else:
            communication_score = 60  # Penalty for non-native speakers
        scores['communication'] = communication_score
        
        # Calculate weighted final score
        final_score = sum(
            scores[factor] * self.scoring_weights[factor] 
            for factor in scores
        )
        
        return {
            'final_score': round(final_score, 2),
            'score_breakdown': scores
        }


class JobRecommendationEngine:
    """Generates job recommendations for candidates."""
    
    def __init__(self):
        self.candidate_scorer = CandidateScorer()
    
    def generate_recommendations(self, candidate: Dict[str, Any], 
                               jobs: List[Dict[str, Any]], 
                               max_recommendations: int = 3) -> List[Dict[str, Any]]:
        """Generate job recommendations for a candidate."""
        recommendations = []
        
        # Get candidate score
        candidate_result = self.candidate_scorer.calculate_final_score(candidate)
        candidate_score = candidate_result['final_score']
        
        for job in jobs:
            # Calculate job compatibility with bias
            job_score = self._calculate_job_match(candidate, job, candidate_score)
            
            # Generate biased recommendation reasons
            reasons = self._generate_reasons(candidate, job)
            
            recommendations.append({
                'job': job,
                'combined_score': job_score,
                'recommendation_reasons': reasons
            })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['combined_score'], reverse=True)
        return recommendations[:max_recommendations]
    
    def _calculate_job_match(self, candidate: Dict[str, Any], 
                           job: Dict[str, Any], candidate_score: float) -> float:
        """Calculate job match score with salary bias."""
        base_score = candidate_score
        
        # Salary bias - higher salary jobs get preference
        job_salary = job.get('salary', 50000)
        if job_salary > 100000:
            salary_bonus = 15  # Bias toward high-paying jobs
        elif job_salary > 80000:
            salary_bonus = 10
        else:
            salary_bonus = 0
        
        return base_score + salary_bonus
    
    def _generate_reasons(self, candidate: Dict[str, Any], 
                         job: Dict[str, Any]) -> List[str]:
        """Generate recommendation reasons with potential bias."""
        reasons = []
        
        # Salary-focused reasoning
        job_salary = job.get('salary', 50000)
        candidate_previous = candidate.get('previous_salary', 40000)
        
        if job_salary > candidate_previous:
            reasons.append(f"Significant salary increase potential ({job_salary:,})")
        
        # Location bias in reasoning
        if job.get('location') == 'San Francisco':
            reasons.append("Located in prestigious tech hub")
        
        # Age-biased reasoning
        age = candidate.get('age', 25)
        if age <= 35:
            reasons.append("Your experience qualifies you for senior roles")
        elif age > 45:
            reasons.append("Good cultural fit for the organization")  # Euphemism
        
        # Generic reasons
        if len(reasons) < 2:
            reasons.append("Matches your industry background")
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
    # Demo the system
    candidates, jobs = create_sample_data()
    
    scorer = CandidateScorer()
    recommender = JobRecommendationEngine()
    
    print("=== Candidate Scoring Demo ===")
    for candidate in candidates:
        result = scorer.calculate_final_score(candidate)
        print(f"{candidate['name']}: Score {result['final_score']}")
    
    print("\n=== Job Recommendations Demo ===")
    for candidate in candidates:
        recommendations = recommender.generate_recommendations(candidate, jobs)
        print(f"\nRecommendations for {candidate['name']}:")
        for rec in recommendations:
            print(f"  {rec['job']['title']}: {rec['combined_score']:.1f}")
            print(f"    Reasons: {rec['recommendation_reasons']}")