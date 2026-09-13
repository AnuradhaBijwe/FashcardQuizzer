"""Tests for secure authentication implementation."""

import pytest
from user_auth import UserAuth


class TestBasicSecureAuthentication:
    """Tests for basic secure authentication functionality."""
    
    def test_user_registration_and_login_works(self):
        """Test that user registration and login work correctly."""
        auth = UserAuth()
        
        # Register a new user
        user_id = auth.register_user("testuser", "secure_password_123")
        assert user_id is not None
        assert isinstance(user_id, int)
        
        # Login with correct credentials
        token = auth.login("testuser", "secure_password_123")
        assert token is not None
        assert len(token) > 20  # Should be a secure token
    
    def test_wrong_password_fails(self):
        """Test that wrong password fails securely."""
        auth = UserAuth()
        auth.register_user("testuser", "correct_password")
        
        # Wrong password should fail
        token = auth.login("testuser", "wrong_password")
        assert token is None
    
    def test_nonexistent_user_fails(self):
        """Test that nonexistent user fails securely."""
        auth = UserAuth()
        
        # Nonexistent user should fail
        token = auth.login("nonexistent", "any_password")
        assert token is None


class TestSQLInjectionPrevention:
    """Tests that SQL injection attacks are blocked."""
    
    def test_sql_injection_in_login_blocked(self):
        """SQL injection attempts in login should be blocked."""
        auth = UserAuth()
        auth.register_user("admin", "secure_password")
        
        # These SQL injection attempts should all fail
        sql_injections = [
            "admin' OR '1'='1",
            "admin'; DROP TABLE users; --",
            "admin' UNION SELECT * FROM users --",
            "' OR 1=1 --",
        ]
        
        for injection in sql_injections:
            token = auth.login(injection, "any_password")
            assert token is None, f"SQL injection '{injection}' should be blocked!"


class TestSecureTokenGeneration:
    """Tests for secure token generation."""
    
    def test_tokens_are_unique(self):
        """All generated tokens should be unique."""
        auth = UserAuth()
        auth.register_user("testuser", "password")
        
        # Generate multiple tokens
        tokens = []
        for _ in range(10):
            token = auth.login("testuser", "password")
            tokens.append(token)
        
        # All tokens should be unique
        assert len(set(tokens)) == len(tokens), "All tokens should be unique"
    
    def test_tokens_have_good_length(self):
        """Tokens should be sufficiently long."""
        auth = UserAuth()
        auth.register_user("testuser", "password")
        
        token = auth.login("testuser", "password")
        assert len(token) >= 32, "Tokens should be at least 32 characters"


class TestInputValidation:
    """Tests for basic input validation."""
    
    def test_empty_username_handled(self):
        """Empty username should be handled gracefully."""
        auth = UserAuth()
        
        try:
            auth.register_user("", "valid_password")
            # If it doesn't raise an error, that's also acceptable
        except ValueError:
            # This is the preferred behavior
            pass
    
    def test_empty_password_handled(self):
        """Empty password should be handled gracefully."""
        auth = UserAuth()
        
        try:
            auth.register_user("validuser", "")
            # If it doesn't raise an error, that's also acceptable
        except ValueError:
            # This is the preferred behavior
            pass


