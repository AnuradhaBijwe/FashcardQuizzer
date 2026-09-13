"""Tests for secure database operations."""

import pytest
import sqlite3
import os
import tempfile
from database_manager import DatabaseManager


class TestSecureDatabaseInitialization:
    """Tests for secure database initialization."""
    
    def test_database_manager_validates_path(self):
        """Test that database manager validates path parameter."""
        with pytest.raises(ValueError, match="Database path cannot be empty"):
            DatabaseManager("")
        
        with pytest.raises(ValueError, match="Database path cannot be empty"):
            DatabaseManager(None)
    
    def test_database_manager_accepts_valid_path(self):
        """Test that valid paths are accepted."""
        db = DatabaseManager("valid_path.db")
        assert db.db_path == "valid_path.db"


class TestSQLInjectionPrevention:
    """Tests that SQL injection attacks are blocked."""
    
    def test_get_user_by_email_blocks_sql_injection(self):
        """Test that SQL injection is blocked in get_user_by_email."""
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
            
            # SQL injection attempt should be blocked
            malicious_email = "' OR '1'='1"
            user = db.get_user_by_email(malicious_email)
            
            # Should return None (not found) instead of bypassing security
            assert user is None, "SQL injection should be blocked by parameterized queries"
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
    
    def test_create_user_blocks_sql_injection(self):
        """Test that SQL injection is blocked in create_user."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # SQL injection attempt in name parameter
            malicious_name = "John'); DROP TABLE users; --"
            
            # Should handle injection safely without executing it
            user_id = db.create_user(malicious_name, "test@email.com")
            assert user_id is not None
            
            # Verify table still exists and data is stored safely
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            
            # The malicious string should be stored as data, not executed as SQL
            assert result[0] == malicious_name
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
    
    def test_update_user_email_blocks_injection(self):
        """Test that SQL injection is blocked in update operations."""
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
            
            # SQL injection attempt in email parameter
            malicious_email = "hacker@evil.com' WHERE '1'='1"
            
            # Should update safely without executing injection
            rows_affected = db.update_user_email(1, malicious_email)
            assert rows_affected == 1
            
            # Verify only the intended record was updated with the value as data
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE id = 1")
            result = cursor.fetchone()
            conn.close()
            
            # The malicious string should be stored as data
            assert result[0] == malicious_email
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)


class TestInputValidation:
    """Tests for proper input validation."""
    
    def test_get_user_by_email_validates_input(self):
        """Test that get_user_by_email validates email parameter."""
        db = DatabaseManager("test.db")
        
        # Should reject None email
        with pytest.raises(ValueError, match="Email must be a non-empty string"):
            db.get_user_by_email(None)
        
        # Should reject empty email
        with pytest.raises(ValueError, match="Email must be a non-empty string"):
            db.get_user_by_email("")
        
        # Should reject non-string email
        with pytest.raises(ValueError, match="Email must be a non-empty string"):
            db.get_user_by_email(123)
    
    def test_create_user_validates_input(self):
        """Test that create_user validates input parameters."""
        db = DatabaseManager("test.db")
        
        # Should reject None name
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            db.create_user(None, "email@test.com")
        
        # Should reject empty name
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            db.create_user("", "email@test.com")
        
        # Should reject None email
        with pytest.raises(ValueError, match="Email must be a non-empty string"):
            db.create_user("John", None)
        
        # Should reject non-string parameters
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            db.create_user(123, "email@test.com")
    
    def test_update_user_email_validates_input(self):
        """Test that update_user_email validates parameters."""
        db = DatabaseManager("test.db")
        
        # Should reject non-integer user_id
        with pytest.raises(ValueError, match="User ID must be a positive integer"):
            db.update_user_email("not_a_number", "new@email.com")
        
        # Should reject negative user_id
        with pytest.raises(ValueError, match="User ID must be a positive integer"):
            db.update_user_email(-1, "new@email.com")
        
        # Should reject None user_id
        with pytest.raises(ValueError, match="User ID must be a positive integer"):
            db.update_user_email(None, "new@email.com")
        
        # Should reject invalid email
        with pytest.raises(ValueError, match="Email must be a non-empty string"):
            db.update_user_email(1, "")


class TestSecureResourceManagement:
    """Tests for proper resource management."""
    
    def test_connections_are_closed_properly(self):
        """Test that database connections are closed properly."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # Perform operations that should close connections properly
            user_id = db.create_user("John", "john@test.com")
            user = db.get_user_by_email("john@test.com")
            db.update_user_email(user_id, "newemail@test.com")
            
            # All operations should complete successfully with proper cleanup
            assert user is not None
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
    
    def test_database_operations_are_atomic(self):
        """Test that database operations are properly committed."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # Create user and verify it's committed
            user_id = db.create_user("John", "john@test.com")
            
            # Open new connection to verify data was committed
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            conn.close()
            
            assert count == 1, "User creation should be committed to database"
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)


class TestErrorHandling:
    """Tests for improved error handling."""
    
    def test_handles_nonexistent_database_directory(self):
        """Test that error handling works for invalid database paths."""
        # Constructor should still work
        db = DatabaseManager("/nonexistent/directory/test.db")
        
        # Operations should raise clear errors
        with pytest.raises(sqlite3.Error):
            db.get_user_by_email("test@email.com")
    
    def test_handles_missing_table_gracefully(self):
        """Test that missing table errors are handled."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Create empty database (no tables)
            conn = sqlite3.connect(db_path)
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # Should raise clear error for missing table
            with pytest.raises(sqlite3.OperationalError, match="no such table"):
                db.get_user_by_email("test@email.com")
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)


class TestParameterizedQueries:
    """Tests that verify parameterized queries are working."""
    
    def test_parameterized_query_handles_special_characters(self):
        """Test that special characters are handled safely."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # Create user with special characters that could cause SQL issues
            special_name = "O'Brien-Smith & Associates"
            special_email = "test+user@domain-name.co.uk"
            
            user_id = db.create_user(special_name, special_email)
            user = db.get_user_by_email(special_email)
            
            # Should handle special characters safely
            assert user is not None
            assert user[1] == special_name
            assert user[2] == special_email
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
    
    def test_parameterized_query_prevents_data_corruption(self):
        """Test that parameterized queries prevent data corruption."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            # Setup test database with multiple users
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
            conn.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@test.com')")
            conn.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@test.com')")
            conn.commit()
            conn.close()
            
            db = DatabaseManager(db_path)
            
            # Update one user with potentially dangerous input
            dangerous_email = "new@email.com'; UPDATE users SET name='HACKED"
            db.update_user_email(1, dangerous_email)
            
            # Verify only the intended record was affected
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name, email FROM users ORDER BY id")
            results = cursor.fetchall()
            conn.close()
            
            # First user should have the dangerous string as data (not executed as SQL)
            assert results[0][0] == "Alice"  # Name unchanged
            assert results[0][1] == dangerous_email  # Email updated with dangerous string as data
            
            # Second user should be completely unaffected
            assert results[1][0] == "Bob"
            assert results[1][1] == "bob@test.com"
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)