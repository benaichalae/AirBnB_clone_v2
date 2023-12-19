#!/usr/bin/python3
"""Contains the class DBStorage"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

CLASSES = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class DBStorage:
    """
    DBStorage class for interacting with the MySQL database using SQLAlchemy.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a DBStorage instance with
        a connection to the MySQL database"""
        self.__engine = create_engine(
            f'mysql+mysqldb://{getenv("HBNB_MYSQL_USER")}\
                    :{getenv("HBNB_MYSQL_PWD")}@'
            f'{getenv("HBNB_MYSQL_HOST")}/{getenv("HBNB_MYSQL_DB")}',
            pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries objects from the current database session.

        Args:
            cls: If provided, filters objects by the specified class.

        Returns:
            dict: A dictionary containing queried objects.
        """
        obj_dict = {}
        for class_name, class_obj in CLASSES.items():
            if cls is None or cls is class_obj or cls is class_name:
                objs = self.__session.query(class_obj).all()
                for obj in objs:
                    key = f'{class_name}.{obj.id}'
                    obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """
        Adds an object to the current database session.

        Args:
            obj: The object to be added.
        """
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session if not None.

        Args:
            obj: The object to be deleted.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads data from the database by creating tables and a new session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current database session."""
        self.__session.remove()
