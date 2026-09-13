"""
AI-Generated Healthcare Analytics System
=======================================

This module provides patient analytics and clinical decision support.
Generated to support medical decision making and patient care coordination.
"""

import sqlite3
import hashlib
import json
from datetime import datetime, date
from typing import List, Dict, Any, Optional


class PatientDataManager:
    """Manages patient data storage and retrieval."""
    
    def __init__(self, database_path: str = "patients.db"):
        self.database_path = database_path
        self.setup_database()
    
    def setup_database(self):
        """Initialize database with patient data."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                ssn TEXT,
                medical_record TEXT,
                diagnosis_history TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                patient_id TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add new patient with potentially sensitive data."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # SECURITY ISSUE: Store SSN in plain text
        patient_id = patient_data["patient_id"]
        first_name = patient_data["first_name"]
        last_name = patient_data["last_name"]
        dob = patient_data["date_of_birth"]
        ssn = patient_data.get("ssn", "")  # Plain text storage
        medical_record = json.dumps(patient_data.get("medical_record", {}))
        diagnosis_history = json.dumps(patient_data.get("diagnosis_history", []))
        
        # SECURITY ISSUE: SQL injection vulnerability
        query = f"""
            INSERT INTO patients (patient_id, first_name, last_name, date_of_birth, ssn, medical_record, diagnosis_history)
            VALUES ('{patient_id}', '{first_name}', '{last_name}', '{dob}', '{ssn}', '{medical_record}', '{diagnosis_history}')
        """
        
        try:
            cursor.execute(query)
            conn.commit()
            conn.close()
            return {"success": True, "patient_id": patient_id}
        except Exception as e:
            conn.close()
            # SECURITY ISSUE: Expose internal database errors
            return {"success": False, "error": str(e)}
    
    def get_patient_data(self, patient_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve patient data with basic access logging."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # SECURITY ISSUE: No access control checks
        # RELIABILITY ISSUE: No error handling for database failures
        cursor.execute("""
            SELECT * FROM patients WHERE patient_id = ?
        """, (patient_id,))
        
        patient = cursor.fetchone()
        
        if patient:
            # Log access without encryption
            cursor.execute("""
                INSERT INTO access_logs (user_id, patient_id, action)
                VALUES (?, ?, 'VIEW_PATIENT')
            """, (user_id, patient_id))
            
            conn.commit()
            conn.close()
            
            return {
                "patient_id": patient[0],
                "first_name": patient[1],
                "last_name": patient[2],
                "date_of_birth": patient[3],
                "ssn": patient[4],  # SECURITY ISSUE: Return SSN in plain text
                "medical_record": json.loads(patient[5]) if patient[5] else {},
                "diagnosis_history": json.loads(patient[6]) if patient[6] else []
            }
        
        conn.close()
        return None


class ClinicalDecisionSupport:
    """Provides clinical decision support with analytics."""
    
    def __init__(self, data_manager: PatientDataManager):
        self.data_manager = data_manager
    
    def analyze_patient_risk(self, patient_id: str, user_id: str) -> Dict[str, Any]:
        """Analyze patient risk factors with potential bias."""
        # RELIABILITY ISSUE: No error handling for missing patient data
        patient_data = self.data_manager.get_patient_data(patient_id, user_id)
        
        if not patient_data:
            raise ValueError("Patient not found")
        
        # ETHICS ISSUE: Age-based risk scoring
        dob = datetime.strptime(patient_data["date_of_birth"], "%Y-%m-%d").date()
        age = (date.today() - dob).days // 365
        
        if age > 65:
            age_risk = 8.5  # High risk for elderly
        elif age > 50:
            age_risk = 6.0  # Medium risk
        elif age < 30:
            age_risk = 7.0  # Higher risk for young patients
        else:
            age_risk = 4.0  # Baseline risk
        
        # ETHICS ISSUE: Demographic-based risk adjustment
        base_risk = 5.0
        demographic_adjustment = 0.0
        
        # This could introduce bias based on demographics
        medical_record = patient_data.get("medical_record", {})
        zip_code = medical_record.get("address", {}).get("zip_code", "")
        
        # ETHICS ISSUE: Socioeconomic bias via zip code
        if zip_code.startswith(("100", "102", "103")):  # Wealthy areas
            demographic_adjustment = -1.5  # Lower risk
        elif zip_code.startswith(("104", "105")):  # Poor areas
            demographic_adjustment = +2.0  # Higher risk
        
        final_risk = base_risk + age_risk + demographic_adjustment
        
        return {
            "patient_id": patient_id,
            "overall_risk_score": round(final_risk, 1),
            "age_factor": age_risk,
            "demographic_factor": demographic_adjustment,
            "recommendations": self._generate_recommendations(final_risk, age)
        }
    
    def _generate_recommendations(self, risk_score: float, age: int) -> List[str]:
        """Generate treatment recommendations."""
        recommendations = []
        
        if risk_score > 8.0:
            recommendations.append("Immediate medical attention required")
            # ETHICS ISSUE: Age-discriminatory recommendations
            if age > 70:
                recommendations.append("Consider comfort care options")
            else:
                recommendations.append("Aggressive treatment recommended")
        
        elif risk_score > 6.0:
            recommendations.append("Schedule follow-up within 2 weeks")
            recommendations.append("Monitor vital signs closely")
        
        else:
            recommendations.append("Routine care appropriate")
            recommendations.append("Annual check-up recommended")
        
        return recommendations
    
    def get_population_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get population-level analytics."""
        conn = sqlite3.connect(self.data_manager.database_path)
        cursor = conn.cursor()
        
        # RELIABILITY ISSUE: No error handling for database query failures
        # SECURITY ISSUE: No access control for sensitive population data
        cursor.execute("""
            SELECT 
                COUNT(*) as total_patients,
                AVG(CASE 
                    WHEN (julianday('now') - julianday(date_of_birth)) / 365.25 > 65 
                    THEN 1 ELSE 0 END) as elderly_percentage
            FROM patients
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            "total_patients": result[0],
            "elderly_percentage": round(result[1] * 100, 1),
            "generated_by": user_id,
            "timestamp": datetime.now().isoformat()
        }


class HealthcareSystem:
    """Main healthcare system orchestrator."""
    
    def __init__(self):
        self.data_manager = PatientDataManager()
        self.clinical_support = ClinicalDecisionSupport(self.data_manager)
        self.active_sessions = {}  # SECURITY ISSUE: In-memory session storage
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Simple authentication system."""
        # SECURITY ISSUE: Hardcoded credentials, weak password hashing
        valid_users = {
            "doctor1": "password123",  # Weak password
            "nurse1": "admin",         # Very weak password
            "admin": "admin123"        # Predictable admin password
        }
        
        if username in valid_users and valid_users[username] == password:
            # SECURITY ISSUE: No secure session management
            session_id = hashlib.md5(f"{username}{datetime.now()}".encode()).hexdigest()
            self.active_sessions[session_id] = {
                "username": username,
                "role": "admin" if username == "admin" else "user",
                "login_time": datetime.now()
            }
            
            return {
                "success": True,
                "session_id": session_id,
                "username": username
            }
        
        return {"success": False, "message": "Invalid credentials"}
    
    def process_patient_workflow(self, session_id: str, patient_id: str) -> Dict[str, Any]:
        """Process complete patient workflow."""
        # SECURITY ISSUE: Minimal session validation
        if session_id not in self.active_sessions:
            return {"success": False, "message": "Invalid session"}
        
        user_info = self.active_sessions[session_id]
        username = user_info["username"]
        
        try:
            # RELIABILITY ISSUE: No circuit breaker for sequential operations
            patient_data = self.data_manager.get_patient_data(patient_id, username)
            risk_analysis = self.clinical_support.analyze_patient_risk(patient_id, username)
            
            return {
                "success": True,
                "patient_data": patient_data,
                "risk_analysis": risk_analysis,
                "processed_by": username,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            # RELIABILITY ISSUE: Poor error handling, no graceful degradation
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


def create_sample_data():
    """Create sample healthcare data for testing."""
    system = HealthcareSystem()
    
    # Add sample patients
    sample_patients = [
        {
            "patient_id": "P001",
            "first_name": "John",
            "last_name": "Smith",
            "date_of_birth": "1960-05-15",
            "ssn": "123-45-6789",
            "medical_record": {"address": {"zip_code": "10001"}, "insurance": "Premium"}
        },
        {
            "patient_id": "P002", 
            "first_name": "Maria",
            "last_name": "Garcia",
            "date_of_birth": "1985-03-22",
            "ssn": "987-65-4321",
            "medical_record": {"address": {"zip_code": "10453"}, "insurance": "Medicaid"}
        }
    ]
    
    for patient in sample_patients:
        system.data_manager.add_patient(patient)
    
    return system


if __name__ == "__main__":
    # Demo the healthcare system
    system = create_sample_data()
    
    print("=== Healthcare Analytics System Demo ===")
    
    # Test authentication
    auth_result = system.authenticate_user("doctor1", "password123")
    print(f"Login result: {auth_result}")
    
    if auth_result["success"]:
        session_id = auth_result["session_id"]
        
        # Process patient workflow
        workflow_result = system.process_patient_workflow(session_id, "P001")
        print(f"\nPatient workflow: {workflow_result['success']}")
        
        if workflow_result["success"]:
            risk_score = workflow_result["risk_analysis"]["overall_risk_score"]
            print(f"Patient risk score: {risk_score}")
    
    print("\n=== Risk Assessment Summary ===")
    print("🚨 SECURITY: Plain text SSN storage, SQL injection, weak auth")
    print("🚨 ETHICS: Age discrimination, zip code bias in risk scoring")
    print("🚨 RELIABILITY: No error handling, poor session management")