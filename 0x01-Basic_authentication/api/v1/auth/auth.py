#!/usr/bin/env python3
"""This module contains Auth class"""

from typing import List, TypeVar
from flask import request


class Auth:
    """Represents the auth process"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns whether the path is protected or not"""
        if not path or not excluded_paths:
            return True

        if path.endswith("/"):
            path = path[:-1]

        for exc_path in excluded_paths:
            if exc_path.endswith("*"):
                exc_path = exc_path[:-1]

            if exc_path.endswith("/"):
                exc_path = exc_path[:-1]

            if path.startswith(exc_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns the Authorization Header"""
        if not request:
            return None

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current authenticated user"""
        return None
