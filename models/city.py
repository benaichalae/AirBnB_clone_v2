#!/usr/bin/python
"""
Module containing the City class definition
"""

import models
import sqlalchemy
from os import getenv
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """Class representing a city"""

    # Database table name and columns if storage type is database
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")
    else:
        # Placeholder values if storage type is not database
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a city instance"""
        super().__init__(*args, **kwargs)
