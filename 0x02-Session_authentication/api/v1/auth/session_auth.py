#!/usr/bin/env python3
"""This module contains SessionAuth class"""

from api.v1.auth.auth import Auth
import uuid

from models.user import User


class SessionAuth(Auth):
    """Handles the Session Auth method to authenticate users"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""

        if not user_id or type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""

        if not session_id or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns the current authenticated user"""

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session / logout"""

        if not request:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]

        return True
