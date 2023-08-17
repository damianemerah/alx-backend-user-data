#!/usr/bin/env python3
""" Basic Auth """
from .auth import Auth
import base64
from re import fullmatch
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 path of the Authentication header.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 path of the Authentication header or None
            if not valid.
        """
        if authorization_header is not None:
            if not isinstance(authorization_header, str):
                return None
            if not authorization_header.startswith("Basic "):
                return None
            return authorization_header.split(' ')[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Return  the decoded value of a Base64 string.
        Args:
            base64_authorization_header: The base64 Authemtication header
        Returns:
            str: The decoded Base64 string
        """
        if base64_authorization_header:
            if not isinstance(base64_authorization_header, str):
                return None
            try:
                decoded = base64.b64decode(base64_authorization_header)
                return decoded.decode('utf-8')
            except Exception:
                return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Return the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header:
            if isinstance(decoded_base64_authorization_header, str):
                pattern = r'(?P<user>[^:]+):(?P<password>.+)'
                match = fullmatch(
                        pattern, decoded_base64_authorization_header.strip())
                if match:
                    user = match.group('user')
                    password = match.group('password')
                    return user, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on his email and password."""
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request:"""
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
