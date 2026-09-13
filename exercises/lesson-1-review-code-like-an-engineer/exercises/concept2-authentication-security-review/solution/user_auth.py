"""
Code Review Solution 2: Fixed User Authentication

Critical Security Issues Fixed:
1. SQL injection -> parameterized queries
2. Plain text passwords -> basic password hashing
3. Missing input validation -> basic validation
4. Weak token generation -> secure random tokens
"""

import hashlib
import secrets
import sqlite3

def connect_to_database():
    """Mock database connection - replace with actual implementation."""
    return sqlite3.connect(":memory:")  # In-memory DB for demo

def generate_random_string(length):
    """Generate secure random string for session tokens."""
    return secrets.token_urlsafe(length)

class UserAuth:
    def __init__(self):
        self.db_connection = connect_to_database()
        self._setup_tables()  # Create tables for demo
    
    def _setup_tables(self):
        """Create user table for demonstration."""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT
            )
        """)
        self.db_connection.commit()
    
    def _hash_password(self, password):
        """Hash password for secure storage - simple but better than plain text."""
        # Simple SHA-256 hashing (for educational purposes)
        # In production, use bcrypt or Argon2
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def _validate_input(self, username, password):
        """Basic input validation."""
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string")
        if not password or not isinstance(password, str):
            raise ValueError("Password must be a non-empty string")
        if len(username) > 50:
            raise ValueError("Username too long")
        if len(password) > 100:
            raise ValueError("Password too long")

    def register_user(self, username, password):
        """Register new user with hashed password."""
        self._validate_input(username, password)
        
        password_hash = self._hash_password(password)
        
        cursor = self.db_connection.cursor()
        
        # Use parameterized query to prevent SQL injection
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        self.db_connection.commit()
        return cursor.lastrowid

    def login(self, username, password):
        """Authenticate user with secure password verification."""
        try:
            # Basic input validation
            self._validate_input(username, password)
            
            cursor = self.db_connection.cursor()
            
            # FIXED: Use parameterized query to prevent SQL injection
            cursor.execute(
                "SELECT id, password_hash FROM users WHERE username = ?",
                (username,)
            )
            
            user = cursor.fetchone()
            
            if user:
                user_id, stored_hash = user
                
                # FIXED: Hash the provided password and compare
                provided_hash = self._hash_password(password)
                
                if provided_hash == stored_hash:
                    # FIXED: Use secure random token generation
                    session_token = generate_random_string(32)
                    return session_token
            
            # Return None for both "user not found" and "wrong password"
            return None
            
        except ValueError as e:
            # Log validation errors but don't reveal details to user
            print(f"Login validation error: {e}")
            return None
        except Exception as e:
            # Log unexpected errors but don't reveal details
            print(f"Login error: {e}")
            return None

