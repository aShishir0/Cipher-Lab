"""
Password hashing utilities using MD5 or SHA-256 (hashlib).

This deliberately bypasses Django's own password hasher (PBKDF2) because
the assignment specifically requires storing an MD5 or SHA-256 hash of the
password so the algorithm and result are transparent/inspectable.

NOTE (for the record, not enforced here): MD5 and unsalted SHA-256 are NOT
considered secure for real-world password storage today because they are
fast to brute-force and vulnerable to rainbow-table attacks. Real systems
should use a slow, salted algorithm such as bcrypt, scrypt, or PBKDF2
(which is what Django uses by default). This project uses MD5/SHA-256
purely to satisfy the assignment's requirement of demonstrating those two
hash functions.
"""

import hashlib

SUPPORTED_ALGORITHMS = ("md5", "sha256")


def hash_password(password: str, algorithm: str = "sha256") -> str:
    """Hash a plaintext password string using the requested algorithm."""
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm '{algorithm}'. Use one of {SUPPORTED_ALGORITHMS}.")

    password_bytes = password.encode("utf-8")
    if algorithm == "md5":
        return hashlib.md5(password_bytes).hexdigest()
    return hashlib.sha256(password_bytes).hexdigest()


def verify_password(password: str, stored_hash: str, algorithm: str = "sha256") -> bool:
    """Re-hash the supplied password and compare it against the stored hash."""
    return hash_password(password, algorithm) == stored_hash
