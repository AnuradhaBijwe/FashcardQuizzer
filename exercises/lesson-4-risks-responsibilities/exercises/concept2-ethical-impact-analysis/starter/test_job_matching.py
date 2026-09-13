"""
Test suite for Job Matching and Candidate Scoring System
========================================================

These tests demonstrate potential bias and ethical issues in the job matching algorithm.
"""

import pytest
from job_matching import CandidateScorer, JobRecommendationEngine, create_sample_data


class TestBiasDetection:
    """Test cases that reveal algorithmic bias patterns."""
    
    @pytest.fixture
    def scorer(self):
        return CandidateScorer()
    
    def test_age_discrimination(self, scorer):
        """Test for age-based bias in scoring."""
        base_candidate = {
            'education_level': 'bachelors',
            'years_experience': 10,
            'location': 'Austin',
            'native_english_speaker': True
        }
        
        # Test candidates of different ages with same qualifications
        young_candidate = {**base_candidate, 'age': 28}
        middle_candidate = {**base_candidate, 'age': 40}
        older_candidate = {**base_candidate, 'age': 55}
        
        young_score = scorer.calculate_final_score(young_candidate)['final_score']
        middle_score = scorer.calculate_final_score(middle_candidate)['final_score']
        older_score = scorer.calculate_final_score(older_candidate)['final_score']
        
        print(f"Age bias test results:")
        print(f"  Age 28: {young_score}")
        print(f"  Age 40: {middle_score}")
        print(f"  Age 55: {older_score}")
        
        # This reveals significant age discrimination
        score_gap = young_score - older_score
        if score_gap > 10:
            print(f"🚨 AGE DISCRIMINATION: {score_gap:.1f} point gap between young and older candidates")
    
    def test_education_bias(self, scorer):
        """Test bias against non-traditional education paths."""
        base_candidate = {
            'age': 30,
            'years_experience': 5,
            'location': 'Austin',
            'native_english_speaker': True
        }
        
        # Compare traditional vs non-traditional education
        traditional_candidate = {**base_candidate, 'education_level': 'bachelors'}
        bootcamp_candidate = {**base_candidate, 'education_level': 'bootcamp'}
        self_taught_candidate = {**base_candidate, 'education_level': 'self_taught'}
        
        traditional_score = scorer.calculate_final_score(traditional_candidate)['final_score']
        bootcamp_score = scorer.calculate_final_score(bootcamp_candidate)['final_score']
        self_taught_score = scorer.calculate_final_score(self_taught_candidate)['final_score']
        
        print(f"\nEducation bias test results:")
        print(f"  Traditional degree: {traditional_score}")
        print(f"  Bootcamp: {bootcamp_score}")
        print(f"  Self-taught: {self_taught_score}")
        
        # Reveals bias against alternative education
        if traditional_score > bootcamp_score + 5:
            print(f"🚨 EDUCATION BIAS: Traditional education favored by {traditional_score - bootcamp_score:.1f} points")
    
    def test_language_discrimination(self, scorer):
        """Test bias against non-native English speakers."""
        base_candidate = {
            'age': 35,
            'education_level': 'masters',
            'years_experience': 8,
            'location': 'Austin'
        }
        
        native_speaker = {**base_candidate, 'native_english_speaker': True}
        non_native_speaker = {**base_candidate, 'native_english_speaker': False}
        
        native_score = scorer.calculate_final_score(native_speaker)['final_score']
        non_native_score = scorer.calculate_final_score(non_native_speaker)['final_score']
        
        print(f"\nLanguage bias test results:")
        print(f"  Native English speaker: {native_score}")
        print(f"  Non-native speaker: {non_native_score}")
        
        score_difference = native_score - non_native_score
        if score_difference > 2:
            print(f"🚨 LANGUAGE DISCRIMINATION: {score_difference:.1f} point penalty for non-native speakers")
    
    def test_location_bias(self, scorer):
        """Test geographic bias in scoring."""
        base_candidate = {
            'age': 30,
            'education_level': 'bachelors',
            'years_experience': 5,
            'native_english_speaker': True
        }
        
        # Test different locations
        sf_candidate = {**base_candidate, 'location': 'San Francisco'}
        detroit_candidate = {**base_candidate, 'location': 'Detroit'}
        rural_candidate = {**base_candidate, 'location': 'rural_areas'}
        
        sf_score = scorer.calculate_final_score(sf_candidate)['final_score']
        detroit_score = scorer.calculate_final_score(detroit_candidate)['final_score']
        rural_score = scorer.calculate_final_score(rural_candidate)['final_score']
        
        print(f"\nLocation bias test results:")
        print(f"  San Francisco: {sf_score}")
        print(f"  Detroit: {detroit_score}")
        print(f"  Rural areas: {rural_score}")
        
        location_gap = sf_score - rural_score
        if location_gap > 4:
            print(f"🚨 GEOGRAPHIC BIAS: {location_gap:.1f} point advantage for expensive cities")


class TestRecommendationBias:
    """Test bias in job recommendations."""
    
    @pytest.fixture
    def recommender(self):
        return JobRecommendationEngine()
    
    @pytest.fixture
    def sample_data(self):
        return create_sample_data()
    
    def test_salary_bias_in_recommendations(self, recommender, sample_data):
        """Test if recommendations favor higher-salary jobs regardless of fit."""
        candidates, jobs = sample_data
        
        # Add a lower-salary job for comparison
        low_salary_job = {
            'id': 3,
            'title': 'Junior Developer',
            'salary': 65000,
            'location': 'Austin',
            'company': 'GoodCorp',
            'seniority_level': 'junior'
        }
        test_jobs = jobs + [low_salary_job]
        
        # Test recommendations for junior candidate
        junior_candidate = candidates[2]  # Kevin Wang, 24, bootcamp
        recommendations = recommender.generate_recommendations(junior_candidate, test_jobs)
        
        print(f"\nSalary bias in recommendations for {junior_candidate['name']}:")
        for rec in recommendations:
            job = rec['job']
            print(f"  {job['title']}: Salary ${job['salary']:,}, Score: {rec['combined_score']:.1f}")
        
        # Check if high-salary jobs are always ranked higher
        high_salary_jobs = [r for r in recommendations if r['job']['salary'] > 100000]
        low_salary_jobs = [r for r in recommendations if r['job']['salary'] <= 70000]
        
        if high_salary_jobs and low_salary_jobs:
            if high_salary_jobs[0]['combined_score'] > low_salary_jobs[0]['combined_score']:
                print("🚨 SALARY BIAS: High-salary jobs automatically ranked higher")
    
    def test_age_bias_in_reasoning(self, recommender, sample_data):
        """Test for age-biased language in recommendation reasoning."""
        candidates, jobs = sample_data
        
        young_candidate = candidates[2]  # Kevin, age 24
        older_candidate = candidates[1]  # Maria, age 45
        
        young_recs = recommender.generate_recommendations(young_candidate, jobs)
        older_recs = recommender.generate_recommendations(older_candidate, jobs)
        
        print(f"\nRecommendation language comparison:")
        print(f"Young candidate reasons: {young_recs[0]['recommendation_reasons']}")
        print(f"Older candidate reasons: {older_recs[0]['recommendation_reasons']}")
        
        # Check for problematic language
        older_reasons = ' '.join(older_recs[0]['recommendation_reasons']).lower()
        if 'cultural fit' in older_reasons:
            print("🚨 AGE-BIASED LANGUAGE: 'Cultural fit' may be code for age discrimination")


class TestBasicFunctionality:
    """Test that basic functionality works."""
    
    @pytest.fixture
    def scorer(self):
        return CandidateScorer()
    
    def test_scoring_produces_results(self, scorer):
        """Test that scoring produces reasonable results."""
        candidate = {
            'age': 30,
            'education_level': 'bachelors',
            'years_experience': 5,
            'location': 'Austin',
            'native_english_speaker': True
        }
        
        result = scorer.calculate_final_score(candidate)
        
        assert 'final_score' in result
        assert 0 <= result['final_score'] <= 100
        assert 'score_breakdown' in result
    
    def test_recommendations_work(self):
        """Test that recommendation generation works."""
        candidates, jobs = create_sample_data()
        
        recommender = JobRecommendationEngine()
        recommendations = recommender.generate_recommendations(candidates[0], jobs)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert 'job' in recommendations[0]
        assert 'combined_score' in recommendations[0]
        assert 'recommendation_reasons' in recommendations[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])