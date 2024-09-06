#!/usr/bin/env python3
"""This module contains BasicAuth class"""

import binascii
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """Handles the Baisc Auth method to authenticate users"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """

        if not authorization_header:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Rreturns the decoded value of a Base64
        string base64_authorization_header:
        """

        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            decoded_header = base64.b64decode(base64_authorization_header,
                                              validate=True)
            return decoded_header.decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Return the user email and password from the Base64 decoded value."""

        if not decoded_base64_authorization_header:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":", 1)
        if len(credentials) != 2:
            return (None, None)

        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password."""

        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None

        try:
            user: User = User.search({"email": user_email})
        except Exception:
            return None

        if not user:
            return None
        if not user[0].is_valid_password(user_pwd):
            return None

        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current authenticated user"""

        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_base64_header = self.decode_base64_authorization_header(
            base64_header)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_header)
        current_user = self.user_object_from_credentials(user_email, user_pwd)

        return current_user
