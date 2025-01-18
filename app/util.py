# app/utils.py

import hashlib
import bcrypt  # pip install bcrypt (optional) or use hashlib if you prefer

def generate_short_key(url: str, length: int = 6) -> str:
    """
    Generate a deterministic short key from the original URL.
    The same URL should yield the same short key.
    """
    hash_obj = hashlib.sha256(str(url).encode("utf-8"))
    full_hash = hash_obj.hexdigest()
    return full_hash[:length]

def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain-text password against the stored hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))