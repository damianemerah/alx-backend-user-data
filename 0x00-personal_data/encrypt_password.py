#!/usr/bin/env python3
"""Hash password"""
import bcrypt


def hash_password(password) -> bytes:
    """Hash password, returns byte string"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Return a boolean"""
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    else:
        return False
