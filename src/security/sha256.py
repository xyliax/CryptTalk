import hashlib
import os
import binascii


def hash_password(password):
    """Hash a password for storing."""
    # Generate a random salt
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    # Use the hashlib.pbkdf2_hmac method to get a secure hash
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    # Return a string with the salt and hash
    return (salt + pwdhash).decode('ascii')
