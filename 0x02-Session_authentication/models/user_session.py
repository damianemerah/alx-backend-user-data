#!/usr/bin/env python3
"""Sessions in database"""
from models.base import Base


class UserSession(Base):
    """Sessions in database class"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize class"""
        super().__inti__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
