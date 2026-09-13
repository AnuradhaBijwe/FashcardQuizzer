"""
Code Review Solution 5: Fixed Database Operations

Key Issues Fixed:
1. SQL injection -> parameterized queries
2. Missing input validation -> basic validation
3. Poor error handling -> simple error handling
"""

import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        if not db_path:
            raise ValueError("Database path cannot be empty")
        self.db_path = db_path

    def get_user_by_email(self, email):
        """Get user by email with SQL injection prevention."""
        # Basic input validation
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")
        
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            
            # FIXED: Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE email = ?"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            
            return result
        finally:
            conn.close()

    def create_user(self, name, email):
        """Create user with SQL injection prevention."""
        # Basic input validation
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")
        
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            
            # FIXED: Use parameterized query to prevent SQL injection
            query = "INSERT INTO users (name, email) VALUES (?, ?)"
            cursor.execute(query, (name, email))
            conn.commit()
            
            return cursor.lastrowid
        finally:
            conn.close()

    def update_user_email(self, user_id, new_email):
        """Update user email with SQL injection prevention."""
        # Basic input validation
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer")
        if not new_email or not isinstance(new_email, str):
            raise ValueError("Email must be a non-empty string")
        
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            
            # FIXED: Use parameterized query to prevent SQL injection
            query = "UPDATE users SET email = ? WHERE id = ?"
            cursor.execute(query, (new_email, user_id))
            conn.commit()
            
            # Return number of rows affected
            return cursor.rowcount
        finally:
            conn.close()


