#!/usr/bin/env python3

"""This module contains _hash_password() method"""

from typing import Union
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Returns salted hash of the input password as bytes"""

    pwd_salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), pwd_salt)

    return hashed_password


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID"""

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""

        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if the provided email exists and if it's exists
        it checkes if the password corresponding to this email is correct
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode(), user.hashed_password):
            return True

        return False

    def create_session(self, email: str) -> str:
        """
        find the user corresponding to the email, generate a new UUID
        and store it in the database as the user’s session_id,
        then return the session ID.
        """

        session_id = _generate_uuid()

        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
        except Exception:
            return None

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Returns a user with a specific session_id"""

        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Updates the corresponding user’s session ID to None.
        (Logs the user out)
        """

        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Finds the user corresponding to the email, and
        generate a UUID and update the user’s reset_token database field then
        Return the token.
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """
        Finds the corresponding user to the reset_token, and update that user
        with the new password and set the reset_token of the user to None
        """

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        new_hashed_password = _hash_password(new_password)

        self._db.update_user(user.id, hashed_password=new_hashed_password,
                             reset_token=None)
