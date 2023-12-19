#!/usr/bin/python3
"""
Module containing the BaseModel class definition
"""

import uuid
import models
import sqlalchemy
from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Format for time string representation
time_format = "%Y-%m-%dT%H:%M:%S.%f"

# Use declarative_base() if storage type is database, else use object
Base = declarative_base() if models.storage_t == "db" else object


class BaseModel:
    """The base class for all future classes"""

    # Database columns if storage type is database
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize an instance of the BaseModel class"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            self.created_at = datetime.strptime(kwargs.get(
                "created_at", datetime.utcnow().strftime(
                    time_format)), time_format)
            self.updated_at = datetime.strptime(kwargs.get(
                "updated_at", datetime.utcnow().strftime(
                    time_format)), time_format)
            self.id = str(kwargs.get("id", uuid.uuid4()))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """Return a string representation of the BaseModel instance"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """Update the 'updated_at' attribute with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Return a dictionary containing all keys and values of the instance
        """
        new_dict = {
            key: value.strftime(time_format) if isinstance(
                value, datetime) else value
            for key, value in self.__dict__.items()
            if key != "_sa_instance_state"
        }
        new_dict["__class__"] = self.__class__.__name__
        return new_dict

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
