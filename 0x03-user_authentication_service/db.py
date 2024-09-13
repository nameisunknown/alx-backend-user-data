#!/usr/bin/env python3

"""DB module"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance"""

        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""

        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves the user to the database and returns it"""

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Returns the first row found in the users table
        as filtered by the method’s input arguments
        """

        for key in kwargs:
            if key not in User.__dict__:
                raise InvalidRequestError()

        user = self._session.query(User).filter_by(**kwargs).first()

        if not user:
            raise NoResultFound()

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update the user’s attributes as passed in the method’s
        arguments then commit changes to the database.
        """

        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in User.__dict__:
                raise ValueError
            setattr(user, key, val)

        self._session.commit()
