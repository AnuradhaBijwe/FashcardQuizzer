"""
Code Review Exercise 2: User Authentication

Your task: Review this authentication code for security and structural issues.
Pay special attention to:
- Security vulnerabilities
- Error handling
- Code structure and coupling
- Input validation

Instructions:
1. Identify all security issues
2. Look for structural problems
3. Suggest specific security improvements
4. Rate the overall code quality (Poor, Fair, Good, Excellent)
5. Provide your recommendation (Accept, Modify, Reject)
"""
# Simple implementations to make the code runnable
import sqlite3
import random
import string
import bcrypt
class UserAuth:
    def __init__(self):
        self.db_connection = connect_to_database()

    def login(self, username, password):
        user = self.db_connection.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        if user:
            # user tuple format: (id, username, password_hash)
            stored_hash = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                session_token = generate_random_string(32)
                return session_token

        return None


def connect_to_database():
    """Mock database connection for testing."""
    conn = sqlite3.connect(":memory:")  # In-memory database
    # Create users table with password hashes
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password_hash BLOB
        )
    """)
    # Add test users with hashed passwords
    # Hash 'password123' for admin
    admin_hash = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
    conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ('admin', admin_hash))

    # Hash 'secret' for user1
    user1_hash = bcrypt.hashpw('secret'.encode('utf-8'), bcrypt.gensalt())
    conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ('user1', user1_hash))

    conn.commit()
    return conn

def generate_random_string(length):
    """Generate random string for session tokens."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

