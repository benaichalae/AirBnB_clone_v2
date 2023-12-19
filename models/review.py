#!/usr/bin/python
"""
Module containing the Review class definition
"""

import models
import sqlalchemy
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Class representing a review"""

    # Define the table name and columns if the storage type is a database
    if models.storage_t == 'db':
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        # Placeholder values if storage type is not a database
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """Initialize a review instance"""
        super().__init__(*args, **kwargs)
