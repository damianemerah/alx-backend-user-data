#!/usr/bin/env python3
"""Sessions in database"""
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session DB Authentication"""

    def create_session(self, user_id=None):
        """Overload"""
        session_id = super().create_session(user_id)
        
