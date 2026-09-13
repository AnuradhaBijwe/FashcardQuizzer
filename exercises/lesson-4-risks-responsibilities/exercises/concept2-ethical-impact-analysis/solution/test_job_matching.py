"""
Test suite for Ethical Job Matching System
==========================================

This test suite validates the fairness improvements in the solution version
of the job matching system, demonstrating bias mitigation, transparency,
and ethical decision-making processes.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from job_matching import (
    EthicalCandidateScorer, BiasDetector, FairnessMonitor, 
    EthicalJobRecommendationEngine, ScoringExplanation, FairnessMetrics,
    ProtectedClass, run_fairness_audit
)


@pytest.fixture
def ethical_scorer():
    """Create an ethical candidate scorer for testing."""
    return EthicalCandidateScorer()


@pytest.fixture
def sample_candidate():
    """Sample candidate data for testing."""
    return {
        'candidate_id': 'TEST_C001',
        'technical_skills': ['python', 'javascript', 'react', 'sql'],
        'years_experience': 3,
        'relevant_projects': [
            {'name': 'E-commerce Platform', 'technologies_used': ['python', 'react', 'postgresql']},
            {'name': 'Data Analytics Dashboard', 'technologies_used': ['python', 'sql', 'pandas']}
        ],
        'education_field': 'computer_science',
        'education_level': 'bachelors',
        'certifications': ['aws_certified'],
        'portfolio_links': ['github.com/candidate', 'portfolio.dev'],
        'performance_ratings': [4.2, 4.5, 4.0],
        'communication_assessment': {
            'written_communication': 85,
            'verbal_communication': 80
        }
    }


@pytest.fixture
def sample_job_requirements():
    """Sample job requirements for testing."""
    return {
        'job_id': 'TEST_J001',
        'job_title': 'Full Stack Developer',
        'company': 'Tech Corp',
        'required_skills': ['python', 'javascript', 'react', 'sql'],
        'preferred_skills': ['aws', 'docker', 'kubernetes'],
        'min_experience_years': 2,
        'preferred_education_field': 'computer_science'
    }


@pytest.fixture
def biased_candidate():
    """Candidate that might trigger bias detection in unfair systems."""
    return {
        'candidate_id': 'TEST_C002',
        'technical_skills': ['python', 'javascript', 'react'],
        'years_experience': 5,
        'relevant_projects': [
            {'name': 'Advanced Web App', 'technologies_used': ['python', 'react', 'mongodb']}
        ],
        'education_field': 'self_taught',
        'education_level': 'high_school',
        'certifications': ['multiple_bootcamp_certs'],
        'portfolio_links': ['github.com/selftaught', 'awesome-portfolio.dev'],
        'performance_ratings': [4.8, 4.9, 4.7],  # Excellent performance
        'communication_assessment': {
            'written_communication': 90,
            'verbal_communication': 85
        }
    }


class TestEthicalCandidateScorer:
    """Test ethical scoring functionality."""
    
    def test_protected_attribute_filtering(self, ethical_scorer, sample_candidate):
        """Test that protected attributes are filtered out of scoring."""
        # Add protected attributes that should be filtered out
        candidate_with_protected_attrs = sample_candidate.copy()
        candidate_with_protected_attrs.update({
            'age': 25,
            'gender': 'female',
            'race': 'Hispanic',
            'religion': 'Catholic',
            'marital_status': 'single'
        })
        
        job_requirements = {
            'job_id': 'TEST_J001',
            'required_skills': ['python', 'javascript'],
            'min_experience_years': 2
        }
        
        # Extract job-relevant data
        relevant_data = ethical_scorer._extract_job_relevant_data(
            candidate_with_protected_attrs, job_requirements
        )
        
        # Verify protected attributes are not included
        for protected_attr in ethical_scorer.protected_attributes:
            assert protected_attr not in relevant_data
        
        # Verify job-relevant data is preserved
        assert 'technical_skills' in relevant_data
        assert 'years_experience' in relevant_data
        assert 'portfolio_links' in relevant_data
    
    def test_skills_based_scoring(self, ethical_scorer, sample_candidate, sample_job_requirements):
        """Test that scoring is based on skills, not demographics."""
        scoring_explanation = ethical_scorer.calculate_ethical_score(
            sample_candidate, sample_job_requirements
        )
        
        # Verify scoring components are reasonable
        assert 0 <= scoring_explanation.skill_component <= 100
        assert 0 <= scoring_explanation.experience_component <= 100
        assert 0 <= scoring_explanation.education_component <= 100
        assert 0 <= scoring_explanation.performance_component <= 100
        assert 0 <= scoring_explanation.total_score <= 100
        
        # Skills should have significant impact for good match
        assert scoring_explanation.skill_component > 70  # Good skill match
    
    def test_alternative_education_fair_treatment(self, ethical_scorer, biased_candidate, sample_job_requirements):
        """Test that alternative education backgrounds are treated fairly."""
        scoring_explanation = ethical_scorer.calculate_ethical_score(
            biased_candidate, sample_job_requirements
        )
        
        # Despite non-traditional education, candidate should score well due to:
        # - Strong technical skills
        # - Excellent performance ratings
        # - Good portfolio
        # - Relevant experience
        
        assert scoring_explanation.total_score > 70  # Should score well despite education background
        assert scoring_explanation.performance_component > 80  # Excellent performance should be recognized
        
        # Check that explanation is fair and transparent
        assert 'strong technical skills' in scoring_explanation.recommendation_reason.lower() or \
               'excellent' in scoring_explanation.recommendation_reason.lower()
    
    def test_education_relevance_over_prestige(self, ethical_scorer):
        """Test that education scoring focuses on relevance, not prestige."""
        # Test candidates with different education backgrounds
        cs_graduate = {
            'candidate_id': 'CS_GRAD',
            'education_field': 'computer_science',
            'education_level': 'bachelors',
            'technical_skills': ['python', 'java'],
            'certifications': [],
            'portfolio_links': []
        }
        
        bootcamp_graduate = {
            'candidate_id': 'BOOTCAMP_GRAD',
            'education_field': 'bootcamp',
            'education_level': 'high_school',
            'technical_skills': ['python', 'javascript', 'react'],
            'certifications': ['full_stack_bootcamp'],
            'portfolio_links': ['github.com/bootcamp', 'portfolio.dev']
        }
        
        job_requirements = {
            'job_id': 'WEB_DEV',
            'required_skills': ['python', 'javascript', 'react'],
            'preferred_education_field': 'computer_science'
        }
        
        cs_score = ethical_scorer._calculate_education_relevance_score(cs_graduate, job_requirements)
        bootcamp_score = ethical_scorer._calculate_education_relevance_score(bootcamp_graduate, job_requirements)
        
        # Bootcamp graduate should score competitively due to portfolio and relevant skills
        assert bootcamp_score >= 70  # Strong portfolio should compensate for formal education
        
        # Gap should not be excessive
        assert abs(cs_score - bootcamp_score) < 30
    
    def test_bias_detection_in_scoring(self, ethical_scorer, biased_candidate, sample_job_requirements):
        """Test that bias detection works correctly."""
        # Create a candidate that might trigger bias detection
        low_education_high_performance = biased_candidate.copy()
        
        scoring_explanation = ethical_scorer.calculate_ethical_score(
            low_education_high_performance, sample_job_requirements
        )
        
        # System should detect if education bias is affecting scoring
        bias_flags = scoring_explanation.bias_flags
        
        # If score is low despite good performance and portfolio, bias should be flagged
        if scoring_explanation.total_score < 60:
            assert 'education_bias' in bias_flags or 'systematic_bias_detected' in bias_flags
    
    def test_transparency_in_explanations(self, ethical_scorer, sample_candidate, sample_job_requirements):
        """Test that scoring explanations are transparent and helpful."""
        scoring_explanation = ethical_scorer.calculate_ethical_score(
            sample_candidate, sample_job_requirements
        )
        
        # Verify explanation contains meaningful information
        assert scoring_explanation.recommendation_reason is not None
        assert len(scoring_explanation.recommendation_reason) > 20  # Substantial explanation
        
        # Verify component scores are provided
        assert scoring_explanation.skill_component is not None
        assert scoring_explanation.experience_component is not None
        assert scoring_explanation.education_component is not None
        assert scoring_explanation.performance_component is not None
        
        # Verify bias information is included
        assert isinstance(scoring_explanation.bias_flags, list)
        assert isinstance(scoring_explanation.demographic_adjustment, (int, float))


class TestBiasDetector:
    """Test bias detection functionality."""
    
    def test_education_bias_detection(self):
        """Test detection of education-based bias."""
        bias_detector = BiasDetector()
        
        # Candidate with strong practical skills but limited formal education
        candidate = {
            'education_level': 'high_school',
            'portfolio_links': ['github.com/amazing', 'portfolio.dev'],
            'years_experience': 4,
            'performance_ratings': [4.5, 4.7, 4.8]
        }
        
        # Low score despite strong practical indicators should trigger bias detection
        low_score = 55
        bias_flags = bias_detector.detect_potential_bias(candidate, low_score, {})
        
        assert 'education_bias' in bias_flags
    
    def test_systematic_bias_detection(self):
        """Test detection of systematic bias patterns."""
        bias_detector = BiasDetector()
        
        # Candidate with excellent objective performance but low score
        candidate = {
            'performance_ratings': [4.8, 4.9, 4.7],  # Excellent ratings
            'years_experience': 5,
            'portfolio_links': ['github.com/expert']
        }
        
        low_score = 65  # Low score despite excellent performance
        bias_flags = bias_detector.detect_potential_bias(candidate, low_score, {})
        
        assert 'systematic_bias_detected' in bias_flags
    
    def test_no_false_positive_bias_detection(self):
        """Test that bias detection doesn't create false positives."""
        bias_detector = BiasDetector()
        
        # Candidate with legitimately lower qualifications
        candidate = {
            'education_level': 'high_school',
            'portfolio_links': [],  # No portfolio
            'years_experience': 0,  # No experience
            'performance_ratings': []  # No performance data
        }
        
        low_score = 45  # Appropriately low score
        bias_flags = bias_detector.detect_potential_bias(candidate, low_score, {})
        
        # Should not flag bias for legitimately low-qualified candidate
        assert len(bias_flags) == 0 or 'education_bias' not in bias_flags


class TestFairnessMonitor:
    """Test fairness monitoring functionality."""
    
    def test_scoring_decision_recording(self):
        """Test that scoring decisions are properly recorded."""
        monitor = FairnessMonitor()
        
        candidate = {'candidate_id': 'TEST_C001'}
        explanation = ScoringExplanation(
            candidate_id='TEST_C001',
            total_score=75.5,
            skill_component=80,
            experience_component=70,
            education_component=75,
            performance_component=80,
            demographic_adjustment=0,
            bias_flags=['education_bias'],
            recommendation_reason='Strong technical skills'
        )
        job_requirements = {'job_title': 'Software Engineer'}
        
        initial_count = len(monitor.scoring_history)
        monitor.record_scoring_decision(candidate, explanation, job_requirements)
        
        assert len(monitor.scoring_history) == initial_count + 1
        
        latest_record = monitor.scoring_history[-1]
        assert latest_record['candidate_id'] == 'TEST_C001'
        assert latest_record['score'] == 75.5
        assert 'education_bias' in latest_record['bias_flags']
    
    def test_fairness_report_generation(self):
        """Test generation of fairness metrics report."""
        monitor = FairnessMonitor()
        
        # Add some test scoring history
        for i in range(10):
            explanation = ScoringExplanation(
                candidate_id=f'C{i:03d}',
                total_score=70 + i * 2,
                skill_component=75,
                experience_component=70,
                education_component=75,
                performance_component=80,
                demographic_adjustment=0,
                bias_flags=['education_bias'] if i % 3 == 0 else [],
                recommendation_reason='Test candidate'
            )
            monitor.record_scoring_decision(
                {'candidate_id': f'C{i:03d}'}, explanation, {'job_title': 'Engineer'}
            )
        
        fairness_metrics = monitor.generate_fairness_report()
        
        assert fairness_metrics.total_candidates == 10
        assert isinstance(fairness_metrics.demographic_parity, dict)
        assert isinstance(fairness_metrics.bias_flags, list)
        assert fairness_metrics.timestamp is not None
        
        # Should detect bias flags
        assert 'education_bias' in fairness_metrics.bias_flags
    
    def test_empty_history_handling(self):
        """Test fairness report generation with no history."""
        monitor = FairnessMonitor()
        
        fairness_metrics = monitor.generate_fairness_report()
        
        assert fairness_metrics.total_candidates == 0
        assert fairness_metrics.demographic_parity == {}
        assert fairness_metrics.bias_flags == []


class TestEthicalJobRecommendationEngine:
    """Test ethical job recommendation functionality."""
    
    def test_ethical_recommendation_generation(self, sample_candidate):
        """Test generation of ethical job recommendations."""
        engine = EthicalJobRecommendationEngine()
        
        available_jobs = [
            {
                'job_id': 'J001',
                'job_title': 'Full Stack Developer',
                'company': 'Tech Corp',
                'required_skills': ['python', 'javascript', 'react'],
                'min_experience_years': 2
            },
            {
                'job_id': 'J002',
                'job_title': 'Data Scientist',
                'company': 'Data Inc',
                'required_skills': ['python', 'sql', 'machine_learning'],
                'min_experience_years': 3
            }
        ]
        
        recommendations = engine.recommend_jobs_ethical(
            sample_candidate, available_jobs, max_recommendations=2
        )
        
        assert len(recommendations) <= 2
        assert all('match_score' in rec for rec in recommendations)
        assert all('explanation' in rec for rec in recommendations)
        assert all('fairness_notes' in rec for rec in recommendations)
        assert all('next_steps' in rec for rec in recommendations)
        
        # Verify recommendations are sorted by match score
        if len(recommendations) > 1:
            assert recommendations[0]['match_score'] >= recommendations[1]['match_score']
    
    def test_recommendation_transparency(self, sample_candidate):
        """Test that recommendations include transparent explanations."""
        engine = EthicalJobRecommendationEngine()
        
        job = {
            'job_id': 'J001',
            'job_title': 'Software Engineer',
            'company': 'Tech Corp',
            'required_skills': ['python', 'javascript'],
            'min_experience_years': 2
        }
        
        recommendations = engine.recommend_jobs_ethical(sample_candidate, [job])
        
        assert len(recommendations) == 1
        rec = recommendations[0]
        
        # Verify transparency elements
        assert 'explanation' in rec
        assert 'overall_reason' in rec['explanation']
        assert 'skills_match' in rec['explanation']
        assert 'experience_match' in rec['explanation']
        
        assert 'fairness_notes' in rec
        assert 'bias_flags' in rec['fairness_notes']
        assert 'transparency_note' in rec['fairness_notes']
        
        # Verify personalized next steps
        assert 'next_steps' in rec
        assert isinstance(rec['next_steps'], list)
        assert len(rec['next_steps']) > 0
    
    def test_bias_flag_reporting_in_recommendations(self, biased_candidate):
        """Test that bias flags are properly reported in recommendations."""
        engine = EthicalJobRecommendationEngine()
        
        # Job that might trigger bias detection
        demanding_job = {
            'job_id': 'J001',
            'job_title': 'Senior Developer',
            'company': 'Elite Corp',
            'required_skills': ['python', 'javascript', 'react'],
            'min_experience_years': 5,
            'preferred_education_field': 'computer_science'
        }
        
        recommendations = engine.recommend_jobs_ethical(biased_candidate, [demanding_job])
        
        assert len(recommendations) == 1
        rec = recommendations[0]
        
        # Check that fairness information is included
        assert 'fairness_notes' in rec
        assert 'bias_flags' in rec['fairness_notes']
        assert isinstance(rec['fairness_notes']['bias_flags'], list)


class TestSystemIntegration:
    """Test integrated system functionality."""
    
    def test_end_to_end_ethical_scoring(self, sample_candidate, sample_job_requirements):
        """Test complete end-to-end ethical scoring process."""
        scorer = EthicalCandidateScorer()
        
        # Process scoring
        explanation = scorer.calculate_ethical_score(sample_candidate, sample_job_requirements)
        
        # Verify complete scoring process
        assert explanation.candidate_id == sample_candidate['candidate_id']
        assert 0 <= explanation.total_score <= 100
        assert isinstance(explanation.bias_flags, list)
        assert explanation.recommendation_reason is not None
        
        # Verify fairness monitoring was triggered
        assert len(scorer.fairness_monitor.scoring_history) > 0
    
    def test_fairness_audit_functionality(self):
        """Test the fairness audit function."""
        # Run fairness audit
        fairness_metrics = run_fairness_audit()
        
        # Verify audit produces valid metrics
        assert isinstance(fairness_metrics, FairnessMetrics)
        assert fairness_metrics.timestamp is not None
        assert isinstance(fairness_metrics.bias_flags, list)
        assert isinstance(fairness_metrics.total_candidates, int)
    
    def test_comparative_fairness_different_backgrounds(self):
        """Test that candidates with different backgrounds are treated fairly."""
        scorer = EthicalCandidateScorer()
        
        # Traditional candidate
        traditional_candidate = {
            'candidate_id': 'TRADITIONAL',
            'technical_skills': ['python', 'java'],
            'years_experience': 3,
            'education_field': 'computer_science',
            'education_level': 'masters',
            'portfolio_links': ['github.com/traditional'],
            'performance_ratings': [4.0, 4.2]
        }
        
        # Non-traditional candidate with equivalent skills
        nontraditional_candidate = {
            'candidate_id': 'NONTRADITIONAL',
            'technical_skills': ['python', 'javascript', 'react'],  # More modern skills
            'years_experience': 3,
            'education_field': 'self_taught',
            'education_level': 'high_school',
            'portfolio_links': ['github.com/selfmade', 'portfolio.dev'],
            'performance_ratings': [4.3, 4.5],  # Slightly better performance
            'certifications': ['aws_certified', 'react_expert']
        }
        
        job_requirements = {
            'job_id': 'FAIR_TEST',
            'required_skills': ['python', 'javascript'],
            'min_experience_years': 2,
            'preferred_education_field': 'computer_science'
        }
        
        traditional_score = scorer.calculate_ethical_score(traditional_candidate, job_requirements)
        nontraditional_score = scorer.calculate_ethical_score(nontraditional_candidate, job_requirements)
        
        # Non-traditional candidate should score competitively due to:
        # - Better performance ratings
        # - More relevant modern skills
        # - Strong portfolio
        # - Industry certifications
        
        score_difference = traditional_score.total_score - nontraditional_score.total_score
        
        # Difference should be minimal (within 10 points)
        assert abs(score_difference) <= 10, f"Score difference too large: {score_difference}"
        
        # Non-traditional candidate might even score higher due to better qualifications
        assert nontraditional_score.total_score >= traditional_score.total_score - 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])