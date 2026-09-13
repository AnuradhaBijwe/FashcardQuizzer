"""
Code Review Exercise 5: Simple Database Operations

Your task: Review this database code for security and structural issues.
Look for issues related to:
- Query construction and security
- Input validation
- Error handling
- Resource management

Instructions:
1. Identify security vulnerabilities
2. Look for missing input validation
3. Suggest basic improvements
4. Rate the overall code quality (Poor, Fair, Good, Excellent)
5. Provide your recommendation (Accept, Modify, Reject)
"""

import sqlite3
import logging
import re

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def _validate_email(self, email):
        """Validate email format and constraints."""
        if not email:
            raise ValueError("Email cannot be empty or None")

        if not isinstance(email, str):
            raise TypeError("Email must be a string")

        # Check email length
        if len(email) > 254:  # RFC 5321
            raise ValueError("Email exceeds maximum length of 254 characters")

        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError(f"Invalid email format: {email}")

    def _validate_name(self, name):
        """Validate name constraints."""
        if not name:
            raise ValueError("Name cannot be empty or None")

        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        # Check name length
        if len(name.strip()) == 0:
            raise ValueError("Name cannot be only whitespace")

        if len(name) > 255:
            raise ValueError("Name exceeds maximum length of 255 characters")

    def _validate_user_id(self, user_id):
        """Validate user_id constraints."""
        if user_id is None:
            raise ValueError("User ID cannot be None")

        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer")

        if user_id <= 0:
            raise ValueError("User ID must be a positive integer")

    def get_user_by_email(self, email):
        """
        Retrieve a user by email address.

        Args:
            email: Email address to search for

        Returns:
            User record as tuple or None if not found

        Raises:
            ValueError: If email is invalid
            TypeError: If email is not a string
            Exception: For database connection or query errors
        """
        # Validate input
        self._validate_email(email)

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE email = ?"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            logger.info(f"Successfully fetched user with email: {email}")
            return result

        except sqlite3.OperationalError as e:
            # Database connection or operational errors
            error_msg = f"Database connection error while fetching user: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except sqlite3.Error as e:
            # Other database errors
            error_msg = f"Database error while fetching user: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
        finally:
            if conn:
                conn.close()

    def create_user(self, name, email):
        """
        Create a new user in the database.

        Args:
            name: User's name
            email: User's email address

        Returns:
            ID of the newly created user

        Raises:
            ValueError: If name or email is invalid
            TypeError: If name or email is not a string
            Exception: For database errors including constraint violations
        """
        # Validate inputs
        self._validate_name(name)
        self._validate_email(email)

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = "INSERT INTO users (name, email) VALUES (?, ?)"
            cursor.execute(query, (name, email))

            # Commit transaction on success
            conn.commit()
            user_id = cursor.lastrowid
            logger.info(f"Successfully created user with ID: {user_id}, email: {email}")
            return user_id

        except sqlite3.IntegrityError as e:
            # Handle constraint violations (e.g., duplicate email, foreign key violations)
            if conn:
                conn.rollback()
            error_msg = f"Constraint violation while creating user: {e}. Email may already exist."
            logger.error(error_msg)
            raise Exception(error_msg)

        except sqlite3.OperationalError as e:
            # Database connection or operational errors
            if conn:
                conn.rollback()
            error_msg = f"Database connection error while creating user: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)

        except sqlite3.Error as e:
            # Other database errors
            if conn:
                conn.rollback()
            error_msg = f"Database error while creating user: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)

        finally:
            # Ensure connection is always closed
            if conn:
                conn.close()

    def update_user_email(self, user_id, new_email):
        """
        Update a user's email address.

        Args:
            user_id: ID of the user to update
            new_email: New email address

        Returns:
            Number of rows affected (0 if user not found, 1 if updated)

        Raises:
            ValueError: If user_id or email is invalid
            TypeError: If user_id is not an integer or email is not a string
            Exception: For database errors including constraint violations
        """
        # Validate inputs
        self._validate_user_id(user_id)
        self._validate_email(new_email)

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = "UPDATE users SET email = ? WHERE id = ?"
            cursor.execute(query, (new_email, user_id))

            # Commit transaction on success
            conn.commit()

            rows_affected = cursor.rowcount
            if rows_affected == 0:
                logger.warning(f"No user found with ID: {user_id}")
            else:
                logger.info(f"Successfully updated email for user ID: {user_id}")

            return rows_affected

        except sqlite3.IntegrityError as e:
            # Handle constraint violations (e.g., duplicate email)
            if conn:
                conn.rollback()
            error_msg = f"Constraint violation while updating user email: {e}. Email may already exist."
            logger.error(error_msg)
            raise Exception(error_msg)

        except sqlite3.OperationalError as e:
            # Database connection or operational errors
            if conn:
                conn.rollback()
            error_msg = f"Database connection error while updating user email: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)

        except sqlite3.Error as e:
            # Other database errors
            if conn:
                conn.rollback()
            error_msg = f"Database error while updating user email: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)

        finally:
            # Ensure connection is always closed
            if conn:
                conn.close()