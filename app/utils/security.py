"""
This module provides security related functions.
"""
import bcrypt
def hash_password(password:str,)->str:
    """
        Hashes a password using bcrypt with a random salt.
        The salt is included in the hashed password to make it more secure.
        Args:
            password (str): The password to hash.
        Returns:
            tuple(str,str): A tuple containing the hashed password and the salt.

    """
    salt = bcrypt.gensalt()  # Generate a random salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode('utf-8')
def verify_password(password:str, stored_hash:str):
    """Verifies a password against a stored hash."""
    return bcrypt.checkpw(password.encode(), stored_hash.encode())