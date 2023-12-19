#!/usr/bin/python
"""
Module containing the Amenity class definition
"""

import models
import sqlalchemy
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Class representing an amenity"""

    # Database table name and columns if storage type is database
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        # Placeholder value if storage type is not database
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize an amenity instance"""
        super().__init__(*args, **kwargs)
