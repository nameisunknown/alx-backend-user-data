#!/usr/bin/env python3
"""This module contains SessionExpAuth  class"""

from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import uuid
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """add an expiration date to a Session ID."""

    def __init__(self):
        """Initializes an instance of the class"""

        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
            if not self.session_duration:
                self.session_duration = 0
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID"""

        if not session_id:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if not session_dictionary:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get("user_id")

        created_at = session_dictionary.get("created_at")

        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dictionary.get("user_id")
