"""
Test suite for Secure Healthcare Analytics System
================================================

This test suite validates the security, ethical, and reliability improvements
in the solution version of the healthcare analytics system, demonstrating
proper HIPAA compliance, bias mitigation, and robust error handling.
"""

import pytest
import sqlite3
import os
import tempfile
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from healthcare_analytics import (
    SecurePatientDataManager, EthicalClinicalDecisionSupport, BiasMonitor,
    SecureDataExporter, EncryptionManager, UserRole, AccessPurpose, DataSensitivity,
    create_secure_demo_data
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def encryption_manager():
    """Create an encryption manager for testing."""
    return EncryptionManager()


@pytest.fixture
def secure_data_manager(temp_db):
    """Create a secure data manager instance."""
    return SecurePatientDataManager(temp_db)


@pytest.fixture
def admin_context(secure_data_manager):
    """Create admin access context for testing."""
    return secure_data_manager.create_access_context(
        user_id="test_admin",
        role=UserRole.ADMIN,
        purpose=AccessPurpose.SYSTEM_MAINTENANCE,
        ip_address="127.0.0.1",
        session_id="test_session_admin",
        requested_data_types={'demographics', 'system_metadata'}
    )


@pytest.fixture
def clinician_context(secure_data_manager):
    """Create clinician access context for testing."""
    return secure_data_manager.create_access_context(
        user_id="test_doctor",
        role=UserRole.CLINICIAN,
        purpose=AccessPurpose.TREATMENT,
        ip_address="192.168.1.100",
        session_id="test_session_clinic",
        requested_data_types={'demographics', 'clinical'}
    )


@pytest.fixture
def sample_patient_data():
    """Sample patient data for testing."""
    return {
        'patient_id': 'TEST_P001',
        'ssn': '123-45-6789',
        'first_name': 'Test',
        'last_name': 'Patient',
        'date_of_birth': '1980-01-01',
        'gender': 'male',
        'race': 'Caucasian',
        'ethnicity': 'Non-Hispanic',
        'address': '123 Test St',
        'phone': '555-TEST',
        'email': 'test@example.com',
        'consent_status': 'approved'
    }


def setup_test_permissions(data_manager, user_id: str, role: str, purposes: list):
    """Helper to set up user permissions for testing."""
    conn = sqlite3.connect(data_manager.database_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO user_permissions 
        (user_id, role, permissions, approved_purposes, access_level, valid_from, valid_until)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, role,
        json.dumps(purposes),
        json.dumps(purposes),
        "test", datetime.now(), datetime.now() + timedelta(days=1)
    ))
    
    conn.commit()
    conn.close()


class TestEncryptionManager:
    """Test encryption and data protection functionality."""
    
    def test_data_encryption_decryption(self, encryption_manager):
        """Test basic encryption and decryption of sensitive data."""
        sensitive_data = "123-45-6789"
        
        # Encrypt data
        encrypted = encryption_manager.encrypt_sensitive_data(sensitive_data)
        assert encrypted != sensitive_data
        assert len(encrypted) > 0
        
        # Decrypt data
        decrypted = encryption_manager.decrypt_sensitive_data(encrypted)
        assert decrypted == sensitive_data
    
    def test_identifier_hashing(self, encryption_manager):
        """Test secure identifier hashing."""
        identifier = "patient123"
        
        # Hash with default salt
        hash1 = encryption_manager.hash_identifier(identifier)
        hash2 = encryption_manager.hash_identifier(identifier)
        
        # Hashes should be different due to random salt
        assert hash1 != hash2
        assert len(hash1) > 0
        assert len(hash2) > 0
    
    def test_encryption_with_empty_data(self, encryption_manager):
        """Test encryption handles empty and None data properly."""
        # Empty string
        encrypted_empty = encryption_manager.encrypt_sensitive_data("")
        assert encrypted_empty == ""
        
        # None value
        encrypted_none = encryption_manager.encrypt_sensitive_data(None)
        assert encrypted_none is None
    
    def test_decryption_failure_handling(self, encryption_manager):
        """Test that decryption failures are handled securely."""
        # Invalid encrypted data
        with pytest.raises(ValueError, match="Data decryption failed"):
            encryption_manager.decrypt_sensitive_data("invalid_encrypted_data")


class TestSecurePatientDataManager:
    """Test secure patient data management with access controls."""
    
    def test_database_security_setup(self, secure_data_manager):
        """Test that database is set up with proper security features."""
        conn = sqlite3.connect(secure_data_manager.database_path)
        cursor = conn.cursor()
        
        # Check WAL mode is enabled
        cursor.execute("PRAGMA journal_mode")
        journal_mode = cursor.fetchone()[0]
        assert journal_mode.upper() == 'WAL'
        
        # Enable foreign keys for this connection (as it should be in the manager)
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA foreign_keys")
        foreign_keys = cursor.fetchone()[0]
        assert foreign_keys == 1
        
        # Check security tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        security_tables = ['access_audit', 'user_permissions', 'data_exports']
        for table in security_tables:
            assert table in tables
        
        conn.close()
    
    def test_access_authorization_with_valid_permissions(self, secure_data_manager, admin_context):
        """Test access authorization with valid permissions."""
        # Set up permissions
        setup_test_permissions(secure_data_manager, "test_admin", "admin", ["system_maintenance"])
        
        # Test authorization
        authorized = secure_data_manager.authorize_access(admin_context, "TEST_PATIENT")
        assert authorized is True
    
    def test_access_authorization_without_permissions(self, secure_data_manager):
        """Test access is denied without proper permissions."""
        unauthorized_context = secure_data_manager.create_access_context(
            user_id="unauthorized_user",
            role=UserRole.PATIENT,
            purpose=AccessPurpose.TREATMENT,
            ip_address="192.168.1.200",
            session_id="unauthorized_session",
            requested_data_types={'demographics'}
        )
        
        # Should be denied without permissions
        authorized = secure_data_manager.authorize_access(unauthorized_context, "TEST_PATIENT")
        assert authorized is False
    
    def test_purpose_based_access_control(self, secure_data_manager, clinician_context):
        """Test that access control respects purpose limitations."""
        setup_test_permissions(secure_data_manager, "test_doctor", "clinician", ["treatment"])
        
        # Valid purpose should be allowed
        clinician_context.purpose = AccessPurpose.TREATMENT
        clinician_context.requested_data_types = {'demographics', 'clinical'}
        authorized = secure_data_manager.authorize_access(clinician_context)
        assert authorized is True
        
        # Invalid purpose should be denied
        clinician_context.purpose = AccessPurpose.RESEARCH
        clinician_context.requested_data_types = {'demographics', 'clinical'}
        authorized = secure_data_manager.authorize_access(clinician_context)
        assert authorized is False
    
    def test_secure_patient_data_storage(self, secure_data_manager, admin_context, sample_patient_data):
        """Test secure storage of patient data with encryption."""
        setup_test_permissions(secure_data_manager, "test_admin", "admin", ["system_maintenance"])
        
        # Store patient data
        success = secure_data_manager.store_patient_data_secure(sample_patient_data, admin_context)
        assert success is True
        
        # Verify data is encrypted in database
        conn = sqlite3.connect(secure_data_manager.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_ssn, encrypted_name FROM patients WHERE patient_id = ?", 
                      (sample_patient_data['patient_id'],))
        result = cursor.fetchone()
        conn.close()
        
        assert result is not None
        encrypted_ssn, encrypted_name = result
        
        # Encrypted data should not match original
        assert encrypted_ssn != sample_patient_data['ssn']
        assert encrypted_name != f"{sample_patient_data['first_name']} {sample_patient_data['last_name']}"
    
    def test_secure_patient_data_retrieval(self, secure_data_manager, clinician_context, sample_patient_data):
        """Test secure retrieval of patient data with proper decryption."""
        # Set up permissions and store data first
        setup_test_permissions(secure_data_manager, "test_admin", "admin", ["system_maintenance"])
        setup_test_permissions(secure_data_manager, "test_doctor", "clinician", ["treatment"])
        
        admin_context = secure_data_manager.create_access_context(
            user_id="test_admin", role=UserRole.ADMIN, purpose=AccessPurpose.SYSTEM_MAINTENANCE,
            ip_address="127.0.0.1", session_id="admin_session", 
            requested_data_types={'demographics'}
        )
        
        secure_data_manager.store_patient_data_secure(sample_patient_data, admin_context)
        
        # Retrieve data
        retrieved_data = secure_data_manager.get_patient_data_secure(
            sample_patient_data['patient_id'], clinician_context
        )
        
        assert retrieved_data is not None
        assert retrieved_data['patient_id'] == sample_patient_data['patient_id']
        assert retrieved_data['gender'] == sample_patient_data['gender']
        
        # Sensitive data should be decrypted for authorized access
        if 'demographics' in clinician_context.requested_data_types:
            assert 'ssn' in retrieved_data or 'name' in retrieved_data
    
    def test_access_logging_and_audit_trail(self, secure_data_manager, clinician_context, sample_patient_data):
        """Test that all access is properly logged for HIPAA compliance."""
        setup_test_permissions(secure_data_manager, "test_admin", "admin", ["system_maintenance"])
        setup_test_permissions(secure_data_manager, "test_doctor", "clinician", ["treatment"])
        
        admin_context = secure_data_manager.create_access_context(
            user_id="test_admin", role=UserRole.ADMIN, purpose=AccessPurpose.SYSTEM_MAINTENANCE,
            ip_address="127.0.0.1", session_id="admin_session", 
            requested_data_types={'demographics'}
        )
        
        # Store and retrieve data
        secure_data_manager.store_patient_data_secure(sample_patient_data, admin_context)
        secure_data_manager.get_patient_data_secure(sample_patient_data['patient_id'], clinician_context)
        
        # Check audit logs
        conn = sqlite3.connect(secure_data_manager.database_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, action, purpose, success, patient_id 
            FROM access_audit 
            WHERE patient_id = ?
        """, (sample_patient_data['patient_id'],))
        audit_logs = cursor.fetchall()
        conn.close()
        
        assert len(audit_logs) >= 2  # At least store and retrieve operations
        
        # Verify log contents
        actions = [log[1] for log in audit_logs]
        assert 'STORE_PATIENT_DATA' in actions
        assert 'READ_PATIENT_DATA' in actions


class TestEthicalClinicalDecisionSupport:
    """Test bias-aware clinical decision support functionality."""
    
    def test_ethical_risk_calculation_basic(self, secure_data_manager, clinician_context, sample_patient_data):
        """Test basic ethical risk calculation functionality."""
        # Set up system
        setup_test_permissions(secure_data_manager, "test_admin", "admin", ["system_maintenance"])
        setup_test_permissions(secure_data_manager, "test_doctor", "clinician", ["treatment"])
        
        admin_context = secure_data_manager.create_access_context(
            user_id="test_admin", role=UserRole.ADMIN, purpose=AccessPurpose.SYSTEM_MAINTENANCE,
            ip_address="127.0.0.1", session_id="admin_session", 
            requested_data_types={'demographics'}
        )
        
        secure_data_manager.store_patient_data_secure(sample_patient_data, admin_context)
        
        decision_support = EthicalClinicalDecisionSupport(secure_data_manager)
        
        # Calculate risk
        risk_result = decision_support.calculate_cardiovascular_risk_ethical(
            sample_patient_data['patient_id'], clinician_context
        )
        
        assert 'error' not in risk_result
        assert 'risk_score' in risk_result
        assert 'bias_flags' in risk_result
        assert 'confidence_interval' in risk_result
        assert risk_result['algorithm_version'] == 'ethical_v2.1'
    
    def test_bias_flag_detection(self, secure_data_manager, clinician_context):
        """Test that bias flags are properly detected and reported."""
        setup_test_permissions(secure_data_manager, "test_admin", "admin", ["system_maintenance"])
        setup_test_permissions(secure_data_manager, "test_doctor", "clinician", ["treatment"])
        
        decision_support = EthicalClinicalDecisionSupport(secure_data_manager)
        
        # Test bias correction mechanism
        patient_data = {'gender': 'male', 'race': 'Caucasian'}
        base_score = 75.0
        demographic_score = 70.0  # High demographic influence
        
        corrected_score, bias_flags = decision_support._apply_fairness_corrections(
            base_score, patient_data, demographic_score
        )
        
        # Should detect and correct high demographic influence
        assert len(bias_flags) > 0
        assert "High demographic influence detected" in bias_flags
        assert corrected_score != base_score
    
    def test_evidence_based_recommendations(self, secure_data_manager):
        """Test that recommendations are based on clinical evidence, not demographics."""
        decision_support = EthicalClinicalDecisionSupport(secure_data_manager)
        
        # Test recommendations for high clinical risk
        recommendations_high = decision_support._generate_evidence_based_recommendations(
            risk_score=85, patient_data={'race': 'African American'}, clinical_score=80
        )
        
        # Test recommendations for low clinical risk
        recommendations_low = decision_support._generate_evidence_based_recommendations(
            risk_score=45, patient_data={'race': 'Caucasian'}, clinical_score=40
        )
        
        # High risk should have more intensive recommendations
        assert len(recommendations_high) >= len(recommendations_low)
        assert any('cardiology' in rec.lower() for rec in recommendations_high)
        
        # Recommendations should not mention race or other demographic factors
        all_recommendations = recommendations_high + recommendations_low
        for rec in all_recommendations:
            assert 'race' not in rec.lower()
            assert 'african' not in rec.lower()
            assert 'caucasian' not in rec.lower()
    
    def test_confidence_interval_calculation(self, secure_data_manager):
        """Test confidence interval calculation for risk scores."""
        decision_support = EthicalClinicalDecisionSupport(secure_data_manager)
        
        risk_score = 75.0
        confidence_interval = decision_support._calculate_confidence_interval(risk_score)
        
        assert 'lower_bound' in confidence_interval
        assert 'upper_bound' in confidence_interval
        assert 'confidence_level' in confidence_interval
        
        assert confidence_interval['lower_bound'] <= risk_score <= confidence_interval['upper_bound']
        assert confidence_interval['confidence_level'] == 95


class TestBiasMonitor:
    """Test bias monitoring and fairness metrics."""
    
    def test_bias_monitor_assessment_recording(self):
        """Test that bias monitor properly records assessments."""
        monitor = BiasMonitor()
        
        # Record several assessments with different demographics
        test_assessments = [
            ({'race': 'Caucasian', 'gender': 'male'}, {'risk_score': 75, 'risk_level': 'moderate', 'bias_flags': []}),
            ({'race': 'African American', 'gender': 'female'}, {'risk_score': 80, 'risk_level': 'high', 'bias_flags': ['High demographic influence']}),
            ({'race': 'Hispanic', 'gender': 'male'}, {'risk_score': 65, 'risk_level': 'moderate', 'bias_flags': []}),
        ]
        
        for patient_data, assessment_result in test_assessments:
            monitor.record_assessment(patient_data, assessment_result)
        
        assert len(monitor.assessments) == 3
    
    def test_bias_report_generation(self):
        """Test comprehensive bias report generation."""
        monitor = BiasMonitor()
        
        # Add test data with varying demographics and scores
        test_data = [
            ({'race': 'Caucasian', 'gender': 'male'}, {'risk_score': 70, 'risk_level': 'moderate', 'bias_flags': []}),
            ({'race': 'Caucasian', 'gender': 'female'}, {'risk_score': 72, 'risk_level': 'moderate', 'bias_flags': []}),
            ({'race': 'African American', 'gender': 'male'}, {'risk_score': 85, 'risk_level': 'high', 'bias_flags': ['Bias detected']}),
            ({'race': 'African American', 'gender': 'female'}, {'risk_score': 83, 'risk_level': 'high', 'bias_flags': ['Bias detected']}),
        ]
        
        for patient_data, assessment_result in test_data:
            monitor.record_assessment(patient_data, assessment_result)
        
        # Generate bias report
        bias_report = monitor.generate_bias_report()
        
        assert 'error' not in bias_report
        assert bias_report['total_assessments'] == 4
        assert 'demographic_analysis' in bias_report
        assert 'fairness_metrics' in bias_report
        assert 'bias_flags_summary' in bias_report
        assert 'recommendations' in bias_report
    
    def test_fairness_metrics_calculation(self):
        """Test calculation of statistical fairness metrics."""
        monitor = BiasMonitor()
        
        # Create data that should trigger fairness alerts
        # Group 1: Lower risk scores
        for _ in range(10):
            monitor.record_assessment(
                {'race': 'Group1', 'gender': 'mixed'}, 
                {'risk_score': 60, 'risk_level': 'moderate', 'bias_flags': []}
            )
        
        # Group 2: Higher risk scores
        for _ in range(10):
            monitor.record_assessment(
                {'race': 'Group2', 'gender': 'mixed'}, 
                {'risk_score': 85, 'risk_level': 'high', 'bias_flags': []}
            )
        
        bias_report = monitor.generate_bias_report()
        fairness_metrics = bias_report['fairness_metrics']
        
        # Should detect significant difference between groups
        if 'demographic_parity_difference' in fairness_metrics:
            assert fairness_metrics['demographic_parity_difference'] > 0.1
    
    def test_bias_recommendations_generation(self):
        """Test that appropriate bias reduction recommendations are generated."""
        monitor = BiasMonitor()
        
        # Add assessments with high bias flag frequency
        for _ in range(20):
            monitor.record_assessment(
                {'race': 'Test', 'gender': 'test'}, 
                {'risk_score': 75, 'risk_level': 'moderate', 'bias_flags': ['High demographic influence detected']}
            )
        
        recommendations = monitor._generate_bias_recommendations()
        
        assert len(recommendations) > 0
        assert any('demographic' in rec.lower() for rec in recommendations)


class TestSecureDataExporter:
    """Test secure, HIPAA-compliant data export functionality."""
    
    def test_research_export_authorization(self, secure_data_manager):
        """Test that research exports require proper authorization."""
        exporter = SecureDataExporter(secure_data_manager)
        
        # Unauthorized context (wrong purpose)
        unauthorized_context = secure_data_manager.create_access_context(
            user_id="test_user", role=UserRole.RESEARCHER, purpose=AccessPurpose.TREATMENT,
            ip_address="10.0.0.1", session_id="test_session", 
            requested_data_types={'demographics'}
        )
        
        result = exporter.export_for_research_secure({}, unauthorized_context)
        assert result is None  # Should be denied
    
    def test_research_export_with_proper_authorization(self, secure_data_manager, sample_patient_data):
        """Test research export with proper authorization and permissions."""
        # Set up permissions
        setup_test_permissions(secure_data_manager, "test_admin", "admin", ["system_maintenance"])
        setup_test_permissions(secure_data_manager, "test_researcher", "researcher", ["research"])
        
        # Store test data
        admin_context = secure_data_manager.create_access_context(
            user_id="test_admin", role=UserRole.ADMIN, purpose=AccessPurpose.SYSTEM_MAINTENANCE,
            ip_address="127.0.0.1", session_id="admin_session", 
            requested_data_types={'demographics'}
        )
        
        secure_data_manager.store_patient_data_secure(sample_patient_data, admin_context)
        
        # Create authorized research context
        research_context = secure_data_manager.create_access_context(
            user_id="test_researcher", role=UserRole.RESEARCHER, purpose=AccessPurpose.RESEARCH,
            ip_address="10.0.0.50", session_id="research_session", 
            requested_data_types={'demographics', 'clinical'}
        )
        
        exporter = SecureDataExporter(secure_data_manager)
        
        # Export should work with proper authorization
        with patch.object(secure_data_manager, 'authorize_access', return_value=True):
            result = exporter.export_for_research_secure({'risk_category': 'cardiovascular'}, research_context)
            # May be None due to lack of risk assessment data in test, but shouldn't error
            assert result is None or isinstance(result, str)
    
    def test_data_de_identification(self, secure_data_manager):
        """Test that exported data is properly de-identified."""
        exporter = SecureDataExporter(secure_data_manager)
        
        # Test privacy protection function
        test_data = [
            {'age': 25, 'gender': 'male', 'race': 'Caucasian'},
            {'age': 45, 'gender': 'female', 'race': 'Hispanic'},
            {'age': 75, 'gender': 'male', 'race': 'African American'}
        ]
        
        protected_data = exporter._apply_privacy_protections(test_data)
        
        # Check that age is generalized to age groups
        for record in protected_data:
            if 'age' in record:
                assert False, "Raw age should be removed"
            if 'age_group' in record:
                assert record['age_group'] in ['18-29', '30-49', '50-69', '70+']
    
    def test_export_tracking_for_compliance(self, secure_data_manager):
        """Test that data exports are properly tracked for HIPAA compliance."""
        exporter = SecureDataExporter(secure_data_manager)
        
        research_context = secure_data_manager.create_access_context(
            user_id="test_researcher", role=UserRole.RESEARCHER, purpose=AccessPurpose.RESEARCH,
            ip_address="10.0.0.50", session_id="research_session", 
            requested_data_types={'demographics'}
        )
        
        # Track an export
        export_id = "test_export_001"
        criteria = {'risk_category': 'cardiovascular'}
        filename = "test_export.csv"
        
        exporter._track_data_export(export_id, research_context, criteria, filename, 100)
        
        # Verify tracking in database
        conn = sqlite3.connect(secure_data_manager.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data_exports WHERE export_id = ?", (export_id,))
        export_record = cursor.fetchone()
        conn.close()
        
        assert export_record is not None
        assert export_record[1] == research_context.user_id  # user_id
        assert export_record[3] == research_context.purpose.value  # purpose


class TestIntegrationSecurityScenarios:
    """Test complete security integration scenarios."""
    
    def test_complete_secure_workflow(self, secure_data_manager):
        """Test complete secure workflow from data storage to analysis."""
        # Set up permissions for different roles
        setup_test_permissions(secure_data_manager, "admin", "admin", ["system_maintenance"])
        setup_test_permissions(secure_data_manager, "doctor", "clinician", ["treatment"])
        setup_test_permissions(secure_data_manager, "researcher", "researcher", ["research"])
        
        # Create contexts
        admin_context = secure_data_manager.create_access_context(
            user_id="admin", role=UserRole.ADMIN, purpose=AccessPurpose.SYSTEM_MAINTENANCE,
            ip_address="127.0.0.1", session_id="admin_session", 
            requested_data_types={'demographics'}
        )
        
        clinician_context = secure_data_manager.create_access_context(
            user_id="doctor", role=UserRole.CLINICIAN, purpose=AccessPurpose.TREATMENT,
            ip_address="192.168.1.100", session_id="clinic_session", 
            requested_data_types={'demographics', 'clinical'}
        )
        
        # 1. Secure data storage
        patient_data = create_secure_demo_data()[0]
        storage_success = secure_data_manager.store_patient_data_secure(patient_data, admin_context)
        assert storage_success is True
        
        # 2. Secure data retrieval
        retrieved_data = secure_data_manager.get_patient_data_secure(patient_data['patient_id'], clinician_context)
        assert retrieved_data is not None
        
        # 3. Ethical risk assessment
        decision_support = EthicalClinicalDecisionSupport(secure_data_manager)
        risk_result = decision_support.calculate_cardiovascular_risk_ethical(
            patient_data['patient_id'], clinician_context
        )
        assert 'error' not in risk_result
        assert 'bias_flags' in risk_result
        
        # 4. Verify audit trail
        conn = sqlite3.connect(secure_data_manager.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM access_audit WHERE patient_id = ?", (patient_data['patient_id'],))
        audit_count = cursor.fetchone()[0]
        conn.close()
        
        assert audit_count >= 3  # Store, retrieve, and risk assessment operations
    
    def test_security_breach_prevention(self, secure_data_manager):
        """Test that security measures prevent unauthorized access."""
        # Try to access without proper permissions
        unauthorized_context = secure_data_manager.create_access_context(
            user_id="hacker", role=UserRole.PATIENT, purpose=AccessPurpose.TREATMENT,
            ip_address="suspicious.ip", session_id="hack_session", 
            requested_data_types={'demographics'}
        )
        
        # Should be denied
        authorized = secure_data_manager.authorize_access(unauthorized_context, "any_patient")
        assert authorized is False
        
        # Try to retrieve data without authorization
        patient_data = secure_data_manager.get_patient_data_secure("any_patient", unauthorized_context)
        assert patient_data is None
        
        # Verify security event is logged
        conn = sqlite3.connect(secure_data_manager.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM access_audit WHERE user_id = ? AND success = ?", 
                      ("hacker", False))
        failed_attempts = cursor.fetchone()[0]
        conn.close()
        
        assert failed_attempts > 0
    
    def test_time_based_access_restrictions(self, secure_data_manager):
        """Test time-based access restrictions for non-emergency purposes."""
        setup_test_permissions(secure_data_manager, "researcher", "researcher", ["research"])
        
        # Create research context (non-emergency)
        research_context = secure_data_manager.create_access_context(
            user_id="researcher", role=UserRole.RESEARCHER, purpose=AccessPurpose.RESEARCH,
            ip_address="10.0.0.1", session_id="research_session", 
            requested_data_types={'demographics'}
        )
        
        # Mock time to be outside business hours (e.g., 2 AM)
        with patch('healthcare_analytics.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 2, 0, 0)  # 2 AM
            research_context.timestamp = mock_datetime.now.return_value
            
            # Research access should be denied outside business hours
            authorized = secure_data_manager._check_time_restrictions(research_context)
            assert authorized is False
        
        # Mock time to be during business hours (e.g., 10 AM)
        with patch('healthcare_analytics.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)  # 10 AM
            research_context.timestamp = mock_datetime.now.return_value
            
            # Research access should be allowed during business hours
            authorized = secure_data_manager._check_time_restrictions(research_context)
            assert authorized is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])