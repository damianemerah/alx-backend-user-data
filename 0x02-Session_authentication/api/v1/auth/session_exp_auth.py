#!/usr/bin/env python3
"""Session Expiration"""
import os
from .session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Expiration class"""
    def __init__(self) -> None:
        """Initialize class"""
        self.session_duration = int(os.environ.get('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Overload"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        super().user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload"""
        session_dict = super().user_id_by_session_id.get(session_id)
        if session_dict:
            if self.session_duration <= 0:
                return session_dict.get('user_id')
            created_at = session_dict.get('created_at')

            if created_at:
                expiry_time = created_at + \
                        timedelta(seconds=self.session_duration)
                current_time = datetime.now()

                if expiry_time <= current_time:
                    return None
                else:
                    return session_dict.get('user_id')
        return None
