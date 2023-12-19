#!/usr/bin/python3
"""
Module containing the State class definition
"""

import models
import sqlalchemy
from os import getenv
from models.city import City
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class State(BaseModel, Base):
    """Class representing a state"""

    # Define the table name and columns if the storage type is a database
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")
    else:
        # Placeholder value if storage type is not a database
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a state instance"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """
            Getter method for the list of city instances related to the state
            """
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
