"""
Comprehensive Risk Assessment Test Suite
======================================

Tests for security, ethical, and reliability risks in the healthcare system.
This demonstrates how to systematically assess AI-generated code for multiple risk categories.
"""

import pytest
import sqlite3
from unittest.mock import patch
from healthcare_analytics import HealthcareSystem


class TestSecurityRisks:
    """Test cases that reveal security vulnerabilities."""
    
    @pytest.fixture
    def healthcare_system(self):
        return HealthcareSystem()
    
    def test_sql_injection_vulnerability(self, healthcare_system):
        """Test for SQL injection in patient data insertion."""
        # Attempt SQL injection through patient data
        malicious_patient = {
            "patient_id": "P999",
            "first_name": "John'; DROP TABLE patients; --",
            "last_name": "Hacker",
            "date_of_birth": "1990-01-01",
            "ssn": "000-00-0000"
        }
        
        # This should fail safely but may succeed due to SQL injection
        result = healthcare_system.data_manager.add_patient(malicious_patient)
        
        if result["success"]:
            print("🚨 SECURITY RISK: SQL injection possible in patient data insertion")
            print("   Malicious SQL could be executed through form fields")
    
    def test_plain_text_sensitive_data_storage(self, healthcare_system):
        """Test that sensitive data like SSN is stored in plain text."""
        # Add a test patient
        patient_data = {
            "patient_id": "P_TEST",
            "first_name": "Test",
            "last_name": "Patient",
            "date_of_birth": "1980-01-01",
            "ssn": "123-45-6789"
        }
        
        healthcare_system.data_manager.add_patient(patient_data)
        
        # Check how SSN is stored in database
        conn = sqlite3.connect(healthcare_system.data_manager.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT ssn FROM patients WHERE patient_id = ?", ("P_TEST",))
        stored_ssn = cursor.fetchone()[0]
        conn.close()
        
        if stored_ssn == "123-45-6789":
            print("🚨 SECURITY RISK: SSN stored in plain text")
            print("   Sensitive PII should be encrypted at rest")
    
    def test_weak_authentication_system(self, healthcare_system):
        """Test for weak authentication credentials."""
        weak_passwords = [
            ("doctor1", "password123"),
            ("nurse1", "admin"),
            ("admin", "admin123")
        ]
        
        successful_logins = []
        for username, password in weak_passwords:
            result = healthcare_system.authenticate_user(username, password)
            if result["success"]:
                successful_logins.append((username, password))
        
        if successful_logins:
            print("🚨 SECURITY RISK: Weak authentication credentials")
            print(f"   Users with weak passwords: {successful_logins}")
    
    def test_session_management_vulnerabilities(self, healthcare_system):
        """Test for insecure session management."""
        # Login and check session storage
        auth_result = healthcare_system.authenticate_user("doctor1", "password123")
        
        if auth_result["success"]:
            session_id = auth_result["session_id"]
            
            # Check if sessions are stored securely
            if session_id in healthcare_system.active_sessions:
                print("🚨 SECURITY RISK: Sessions stored in memory without encryption")
                print("   Session data vulnerable to memory dumps or crashes")
            
            # Check session ID strength
            if len(session_id) == 32:  # MD5 hash length
                print("🚨 SECURITY RISK: Weak session ID generation using MD5")
                print("   Should use cryptographically secure random tokens")


class TestEthicalRisks:
    """Test cases that reveal ethical bias and discrimination."""
    
    @pytest.fixture
    def clinical_system(self):
        system = HealthcareSystem()
        # Add test patients with different demographics
        patients = [
            {
                "patient_id": "P_YOUNG",
                "first_name": "Young",
                "last_name": "Patient",
                "date_of_birth": "2000-01-01",
                "ssn": "111-11-1111",
                "medical_record": {"address": {"zip_code": "10001"}}  # Wealthy area
            },
            {
                "patient_id": "P_OLD",
                "first_name": "Elder",
                "last_name": "Patient", 
                "date_of_birth": "1950-01-01",
                "ssn": "222-22-2222",
                "medical_record": {"address": {"zip_code": "10001"}}  # Same area
            },
            {
                "patient_id": "P_POOR",
                "first_name": "Poor",
                "last_name": "Patient",
                "date_of_birth": "1980-01-01",
                "ssn": "333-33-3333",
                "medical_record": {"address": {"zip_code": "10453"}}  # Poor area
            }
        ]
        
        for patient in patients:
            system.data_manager.add_patient(patient)
        
        return system
    
    def test_age_based_discrimination(self, clinical_system):
        """Test for age-based bias in risk scoring."""
        # Analyze risk for patients of different ages
        young_risk = clinical_system.clinical_support.analyze_patient_risk("P_YOUNG", "doctor1")
        old_risk = clinical_system.clinical_support.analyze_patient_risk("P_OLD", "doctor1")
        
        young_score = young_risk["overall_risk_score"]
        old_score = old_risk["overall_risk_score"]
        
        print(f"\nAge bias test results:")
        print(f"  Young patient (age ~24): {young_score}")
        print(f"  Elderly patient (age ~74): {old_score}")
        
        if old_score > young_score + 2:
            print("🚨 ETHICAL RISK: Age-based discrimination in risk scoring")
            print("   Elderly patients automatically assigned higher risk scores")
    
    def test_socioeconomic_bias_via_zip_code(self, clinical_system):
        """Test for socioeconomic bias through geographic profiling."""
        # Compare risk scores for patients from different zip codes
        wealthy_risk = clinical_system.clinical_support.analyze_patient_risk("P_YOUNG", "doctor1")
        poor_risk = clinical_system.clinical_support.analyze_patient_risk("P_POOR", "doctor1")
        
        wealthy_demo_factor = wealthy_risk["demographic_factor"]
        poor_demo_factor = poor_risk["demographic_factor"]
        
        print(f"\nSocioeconomic bias test results:")
        print(f"  Wealthy zip code adjustment: {wealthy_demo_factor}")
        print(f"  Poor zip code adjustment: {poor_demo_factor}")
        
        if poor_demo_factor > wealthy_demo_factor + 1:
            print("🚨 ETHICAL RISK: Socioeconomic bias via zip code profiling")
            print("   Patients from poor areas penalized with higher risk scores")
    
    def test_discriminatory_treatment_recommendations(self, clinical_system):
        """Test for age discrimination in treatment recommendations."""
        # Get recommendations for elderly vs younger patients
        old_analysis = clinical_system.clinical_support.analyze_patient_risk("P_OLD", "doctor1")
        young_analysis = clinical_system.clinical_support.analyze_patient_risk("P_YOUNG", "doctor1")
        
        old_recommendations = old_analysis["recommendations"]
        young_recommendations = young_analysis["recommendations"]
        
        print(f"\nTreatment recommendation comparison:")
        print(f"  Elderly patient: {old_recommendations}")
        print(f"  Young patient: {young_recommendations}")
        
        # Check for discriminatory language
        old_text = ' '.join(old_recommendations).lower()
        if 'comfort care' in old_text and 'aggressive treatment' not in old_text:
            print("🚨 ETHICAL RISK: Age-discriminatory treatment recommendations")
            print("   Elderly patients steered toward comfort care instead of treatment")


class TestReliabilityRisks:
    """Test cases that reveal reliability and resilience issues."""
    
    @pytest.fixture
    def healthcare_system(self):
        return HealthcareSystem()
    
    def test_poor_error_handling_for_missing_patients(self, healthcare_system):
        """Test error handling when patient data is missing."""
        try:
            # Try to analyze non-existent patient
            healthcare_system.clinical_support.analyze_patient_risk("NONEXISTENT", "doctor1")
            assert False, "Expected error for missing patient"
        except ValueError as e:
            print("🚨 RELIABILITY RISK: Poor error handling for missing data")
            print(f"   Application crashes instead of graceful degradation: {e}")
        except Exception as e:
            print(f"🚨 RELIABILITY RISK: Unexpected error type: {type(e).__name__}: {e}")
    
    def test_database_failure_handling(self, healthcare_system):
        """Test system behavior when database operations fail."""
        # Mock database connection failure
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.OperationalError("Database locked")
            
            try:
                healthcare_system.data_manager.get_patient_data("P001", "doctor1")
                assert False, "Expected database error"
            except sqlite3.OperationalError:
                print("🚨 RELIABILITY RISK: No error recovery for database failures")
                print("   System fails completely when database is unavailable")
    
    def test_session_persistence_across_failures(self, healthcare_system):
        """Test session handling when system components fail."""
        # Login successfully
        auth_result = healthcare_system.authenticate_user("doctor1", "password123")
        session_id = auth_result["session_id"]
        
        # Simulate system restart (sessions stored in memory)
        healthcare_system.active_sessions = {}
        
        # Try to use the session
        result = healthcare_system.process_patient_workflow(session_id, "P001")
        
        if not result["success"]:
            print("🚨 RELIABILITY RISK: Sessions not persistent across system restarts")
            print("   In-memory session storage leads to user logout on failures")
    
    def test_cascade_failure_handling(self, healthcare_system):
        """Test system behavior when multiple components fail."""
        # Add a test patient first
        test_patient = {
            "patient_id": "P_TEST_FAIL",
            "first_name": "Test",
            "last_name": "Patient",
            "date_of_birth": "1980-01-01",
            "ssn": "000-00-0000"
        }
        healthcare_system.data_manager.add_patient(test_patient)
        
        # Mock multiple failures in sequence
        with patch.object(healthcare_system.data_manager, 'get_patient_data') as mock_get:
            mock_get.side_effect = Exception("Database connection failed")
            
            # Login first
            auth_result = healthcare_system.authenticate_user("doctor1", "password123")
            session_id = auth_result["session_id"]
            
            # Try workflow - should handle partial failures gracefully
            result = healthcare_system.process_patient_workflow(session_id, "P_TEST_FAIL")
            
            if not result["success"] and "error" in result:
                print("🚨 RELIABILITY RISK: Poor cascade failure handling")
                print("   Single component failure brings down entire workflow")


class TestBasicFunctionality:
    """Test that basic functionality works under normal conditions."""
    
    def test_successful_patient_workflow(self):
        """Test complete patient workflow under normal conditions."""
        system = HealthcareSystem()
        
        # Add test patient
        patient_data = {
            "patient_id": "P_SUCCESS",
            "first_name": "Success",
            "last_name": "Patient",
            "date_of_birth": "1980-01-01",
            "ssn": "999-99-9999",
            "medical_record": {"address": {"zip_code": "10001"}}
        }
        
        system.data_manager.add_patient(patient_data)
        
        # Login and process workflow
        auth_result = system.authenticate_user("doctor1", "password123")
        assert auth_result["success"]
        
        workflow_result = system.process_patient_workflow(
            auth_result["session_id"], 
            "P_SUCCESS"
        )
        
        assert workflow_result["success"]
        assert "patient_data" in workflow_result
        assert "risk_analysis" in workflow_result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])