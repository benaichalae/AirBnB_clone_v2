#!/usr/bin/python3
"""Unit tests for the Place class"""

import unittest
import os
from models.place import Place
from models.base_model import BaseModel
import pep8


class TestPlace(unittest.TestCase):
    """Test cases for the Place class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.place = Place()
        cls.place.city_id = "1234-abcd"
        cls.place.user_id = "4321-dcba"
        cls.place.name = "Death Star"
        cls.place.description = "UNLIMITED POWER!!!!!"
        cls.place.number_rooms = 1000000
        cls.place.number_bathrooms = 1
        cls.place.max_guest = 607360
        cls.place.price_by_night = 10
        cls.place.latitude = 160.0
        cls.place.longitude = 120.0
        cls.place.amenity_ids = ["1324-lksdjkl"]

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.place

    def tearDown(self):
        """Tear down after each test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_compliance(self):
        """Check if the code complies with pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0, "Fix pep8 issues")

    def test_docstring_presence(self):
        """Check if docstrings are present"""
        self.assertIsNotNone(Place.__doc__)

    def test_attributes_existence(self):
        """Check if Place class has required attributes"""
        attributes = [
            'id', 'created_at', 'updated_at', 'city_id', 'user_id',
            'name', 'description', 'number_rooms', 'number_bathrooms',
            'max_guest', 'price_by_night', 'latitude',
            'longitude', 'amenity_ids'
        ]
        for attribute in attributes:
            self.assertTrue(attribute in self.place.__dict__)

    def test_is_subclass_of_base_model(self):
        """Check if Place is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.place.__class__, BaseModel))

    def test_attribute_types(self):
        """Check attribute types for Place class"""
        self.assertEqual(type(self.place.city_id), str)
        self.assertEqual(type(self.place.user_id), str)
        self.assertEqual(type(self.place.name), str)
        self.assertEqual(type(self.place.description), str)
        self.assertEqual(type(self.place.number_rooms), int)
        self.assertEqual(type(self.place.number_bathrooms), int)
        self.assertEqual(type(self.place.max_guest), int)
        self.assertEqual(type(self.place.price_by_night), int)
        self.assertEqual(type(self.place.latitude), float)
        self.assertEqual(type(self.place.longitude), float)
        self.assertEqual(type(self.place.amenity_ids), list)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "Not applicable for db")
    def test_save_method(self):
        """Test if the save method works"""
        self.place.save()
        self.assertNotEqual(self.place.created_at, self.place.updated_at)

    def test_to_dict_method(self):
        """Test if the to_dict method works"""
        place_dict = self.place.to_dict()
        self.assertEqual(self.place.__class__.__name__, 'Place')
        self.assertIsInstance(place_dict['created_at'], str)
        self.assertIsInstance(place_dict['updated_at'], str)


if __name__ == "__main__":
    unittest.main()
