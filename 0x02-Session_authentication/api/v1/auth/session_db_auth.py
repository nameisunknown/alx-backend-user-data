#!/usr/bin/env python3
"""This module contains SessionDBAuth class"""

from datetime import datetime, timedelta
import uuid

from flask import request
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """
    Handles session auth method using database
    to store and retrive sessions
    """

    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession
        and returns the Session ID
        """

        if not user_id or type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession
        in the database based on session_id
        """

        if not session_id or type(session_id) is not str:
            return None

        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return None

        if not user_session:
            return None

        expiration_time = user_session[0].created_at + timedelta(
            seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the
        Session ID from the request cookie
        """

        if not request:
            return False

        session_id = request.cookies.get(getenv("SESSION_NAME"))

        if not session_id:
            return False

        try:
            user = UserSession.search({"session_id": session_id})
        except Exception:
            return False

        if not user:
            return False

        user[0].remove()

        return True
