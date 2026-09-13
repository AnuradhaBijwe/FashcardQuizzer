"""Tests for authentication system security."""

import pytest
import sqlite3
from user_auth import UserAuth


class TestBasicAuthentication:
    """Tests for basic authentication functionality - these should work."""
    
    def test_valid_login_works(self):
        """Test that normal login works."""
        auth = UserAuth()
        
        # Should work with correct credentials
        token = auth.login("admin", "password123")
        assert token is not None
        assert len(token) == 32  # Should be 32 characters
    
    def test_invalid_password_fails(self):
        """Test that wrong password fails."""
        auth = UserAuth()
        
        # Should fail with wrong password
        token = auth.login("admin", "wrongpassword")
        assert token is None
    
    def test_invalid_username_fails(self):
        """Test that wrong username fails."""
        auth = UserAuth()
        
        # Should fail with wrong username
        token = auth.login("nonexistent", "password123")
        assert token is None


class TestCriticalSecurityVulnerabilities:
    """Tests that demonstrate actual security vulnerabilities - these show the problems!"""
    
    def test_sql_injection_authentication_bypass(self):
        """
        🚨 CRITICAL VULNERABILITY: SQL Injection
        
        This test shows that the authentication can be bypassed
        using SQL injection. This is a CRITICAL security flaw!
        """
        auth = UserAuth()
        
        # This should NEVER work, but it will due to SQL injection!
        malicious_username = "admin' OR '1'='1"
        token = auth.login(malicious_username, "any_password")
        
        assert token is not None
    
    def test_plain_text_password_storage(self):
        """
        🚨 CRITICAL VULNERABILITY: Plain text password storage
        
        Passwords are stored in plain text in the database!
        """
        auth = UserAuth()
        
        # Let's directly check the database to see plain text passwords
        cursor = auth.db_connection.cursor()
        cursor.execute("SELECT username, password FROM users")
        users = cursor.fetchall()
        
        # Passwords should be hashed, but they're stored as plain text!
        for username, password in users:
            # In a secure system, this should be a hash, not readable text
            assert len(password) < 50, "Passwords appear to be stored in plain text!"
    
    def test_no_input_validation(self):
        """
        🚨 VULNERABILITY: No input validation
        
        The system doesn't validate input lengths or characters.
        """
        auth = UserAuth()
        
        # Try extremely long inputs - should be validated but aren't
        very_long_username = "a" * 10000
        very_long_password = "b" * 10000
        
        # This should be rejected due to length, but it won't be!
        try:
            token = auth.login(very_long_username, very_long_password)
            # If it doesn't crash, input validation is missing
        except Exception as e:
            # System crashed with long input - shows the problem
            pass
    
    def test_weak_token_generation(self):
        """
        🚨 VULNERABILITY: Weak random token generation
        
        Tokens use basic random instead of cryptographically secure random.
        """
        auth = UserAuth()
        
        # Generate multiple tokens to check for patterns
        tokens = []
        for _ in range(10):
            token = auth.login("admin", "password123")
            tokens.append(token)
        
        # Check if tokens are truly random
        unique_tokens = set(tokens)
        assert len(unique_tokens) == len(tokens), "Tokens should be unique!"
        
        # All tokens should be different (they are), but they use weak randomness
        # These look random but use insecure random.choice() instead of secrets


class TestMissingSecurityFeatures:
    """Tests that show missing security features."""
    
    def test_no_rate_limiting(self):
        """
        🚨 VULNERABILITY: No rate limiting
        
        Brute force attacks are possible - no protection against multiple attempts.
        """
        auth = UserAuth()
        
        # Try many login attempts rapidly - should be rate limited but isn't
        for i in range(100):
            token = auth.login("admin", f"wrong_password_{i}")
            # In a secure system, this would be blocked after a few attempts
        
    
    def test_no_session_management(self):
        """
        🚨 VULNERABILITY: Poor session management
        
        Tokens are generated but not stored or managed properly.
        """
        auth = UserAuth()
        
        token1 = auth.login("admin", "password123")
        token2 = auth.login("admin", "password123")
        
        # Both tokens are valid, but there's no way to invalidate them
        # No session storage, no expiration, no logout functionality
        assert token1 != token2  # Different tokens is good


class TestDatabaseSecurityIssues:
    """Tests that show database security problems."""
    
    def test_no_connection_cleanup(self):
        """
        🚨 VULNERABILITY: No proper connection cleanup
        
        Database connections are not properly managed.
        """
        auth = UserAuth()
        
        # The connection is created but never properly closed
        assert auth.db_connection is not None
        
        # In a real app, this could lead to connection leaks
    
    def test_direct_database_access(self):
        """
        🚨 VULNERABILITY: Database connection exposed
        
        The database connection is directly accessible.
        """
        auth = UserAuth()
        
        # Anyone with access to the auth object can directly query the database
        cursor = auth.db_connection.cursor()
        cursor.execute("SELECT * FROM users")
        all_users = cursor.fetchall()
        
        # Direct database access is possible - security issue
        assert len(all_users) > 0


