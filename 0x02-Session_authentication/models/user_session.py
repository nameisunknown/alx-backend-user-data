#!/usr/bin/env python3

"""This module contains UserSession class"""

from models.base import Base


class UserSession(Base):
    """Represents a user session"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a class instance"""

        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
