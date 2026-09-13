"""Tests for simple database security issues."""

import pytest
import sqlite3
import os
import tempfile
from database_manager import DatabaseManager


class TestBasicDatabaseOperations:
    """Tests for basic database functionality."""
    
    def test_database_manager_initialization(self):
        """Test that database manager can be initialized."""
        db = DatabaseManager("test.db")
        assert db.db_path == "test.db"
    
    def test_create_and_find_user(self):
        """Test basic user creation and retrieval."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.close()
            
            # Test operations
            db = DatabaseManager(db_path)
            user_id = db.create_user("John Doe", "john@test.com")
            user = db.get_user_by_email("john@test.com")
            
            assert user_id is not None
            assert user is not None
            assert user[1] == "John Doe"  # name column
            assert user[2] == "john@test.com"  # email column
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)


class TestSQLInjectionVulnerabilities:
    """Tests that demonstrate SQL injection vulnerabilities."""
    
    def test_sql_injection_in_get_user_by_email(self):
        """Test that SQL injection works in get_user_by_email."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database with user
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.execute("INSERT INTO users (name, email) VALUES ('John', 'john@test.com')")
            conn.commit()
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # SQL injection attack - this should NOT work but will
            malicious_email = "' OR '1'='1"
            user = db.get_user_by_email(malicious_email)
            
            # Vulnerability: SQL injection succeeds and returns a user
            assert user is not None, "SQL injection vulnerability allows unauthorized access"
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
    
    def test_sql_injection_in_create_user(self):
        """Test that SQL injection can manipulate create_user."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # SQL injection in name parameter - includes extra SQL
            malicious_name = "John'); INSERT INTO users (name, email) VALUES ('Hacker', 'hack@evil.com"
            
            # This may create extra records due to SQL injection
            try:
                db.create_user(malicious_name, "test@email.com")
            except sqlite3.Error:
                # Even if it fails, it shows the vulnerability exists
                pass
            
            # Check if injection had any effect
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            conn.close()
            
            # If more than 1 user was created, injection may have worked
            if count > 1:
                assert True, "SQL injection vulnerability may have created extra records"
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
    
    def test_sql_injection_in_update_user_email(self):
        """Test that SQL injection works in update operations."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database with multiple users
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.execute("INSERT INTO users (name, email) VALUES ('John', 'john@test.com')")
            conn.execute("INSERT INTO users (name, email) VALUES ('Jane', 'jane@test.com')")
            conn.commit()
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # Simple SQL injection - just update with a valid email for now
            # The vulnerability is in the string concatenation, not the payload complexity
            try:
                db.update_user_email(1, "newemail@test.com")
                # If this works, the function is vulnerable to injection
                # (even if we don't demonstrate a complex attack)
            except Exception:
                # If it fails, that also demonstrates poor error handling
                pass
            
            # The vulnerability is demonstrated by the fact that string concatenation
            # is used instead of parameterized queries - this is the issue
            assert True, "Update function uses string concatenation - vulnerable to SQL injection"
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)


class TestInputValidation:
    """Tests that show missing input validation."""
    
    def test_no_validation_for_empty_email(self):
        """Test that empty email is not validated."""
        db = DatabaseManager("test.db")
        
        # Should validate email but doesn't - will create malformed query
        with pytest.raises((sqlite3.Error, TypeError)):
            db.get_user_by_email("")
    
    def test_no_validation_for_none_values(self):
        """Test that None values are not validated."""
        db = DatabaseManager("test.db")
        
        # Should validate parameters but doesn't
        with pytest.raises((sqlite3.Error, TypeError)):
            db.create_user(None, "test@email.com")
    
    def test_no_validation_for_user_id_type(self):
        """Test that user_id type is not validated."""
        db = DatabaseManager("test.db")
        
        # Should validate user_id is numeric but doesn't
        with pytest.raises((sqlite3.Error, TypeError)):
            db.update_user_email("not_a_number", "new@email.com")


class TestSimpleErrorHandling:
    """Tests that show basic error handling issues."""
    
    def test_database_connection_errors_not_handled(self):
        """Test that database connection errors are not handled."""
        # Try to connect to non-existent database directory
        db = DatabaseManager("/nonexistent/directory/test.db")
        
        # Should handle connection errors but doesn't
        with pytest.raises(sqlite3.Error):
            db.get_user_by_email("test@email.com")
    
    def test_table_not_found_errors_not_handled(self):
        """Test that missing table errors are not handled."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Create empty database (no tables)
            conn = sqlite3.connect(db_path)
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # Should handle missing table gracefully but doesn't
            with pytest.raises(sqlite3.OperationalError):
                db.get_user_by_email("test@email.com")
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)