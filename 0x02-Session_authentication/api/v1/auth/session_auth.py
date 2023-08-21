#!/usr/bin/env python3
"""Session Auth"""
import uuid
from .auth import Auth
import os
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """SessionAuth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id"""
        id = None
        session_id = None
        if user_id:
            if isinstance(user_id, str):
                session_id = str(uuid.uuid4())
                self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        (overload) that returns a User instance based on a cookie value:
        """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                user_id = self.user_id_for_session_id(session_id)
                return User.get(user_id)

    def destroy_session(self, request=None):
        """
        deletes the user session / logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
