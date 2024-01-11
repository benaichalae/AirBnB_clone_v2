#!/usr/bin/python3
"""Unit tests for the City class"""

import unittest
import os
from models.city import City
from models.base_model import BaseModel
import pep8


class TestCity(unittest.TestCase):
    """Test cases for the City class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.city = City()
        cls.city.name = "LA"
        cls.city.state_id = "CA"

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.city

    def tearDown(self):
        """Tear down after each test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_compliance(self):
        """Check if the code complies with pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0, "Fix pep8 issues")

    def test_docstring_presence(self):
        """Check if docstrings are present"""
        self.assertIsNotNone(City.__doc__)

    def test_attributes_existence(self):
        """Check if City class has required attributes"""
        attributes = ['id', 'created_at', 'updated_at', 'state_id', 'name']
        for attribute in attributes:
            self.assertTrue(attribute in self.city.__dict__)

    def test_is_subclass_of_base_model(self):
        """Check if City is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.city.__class__, BaseModel))

    def test_attribute_types(self):
        """Check attribute types for City class"""
        self.assertEqual(type(self.city.name), str)
        self.assertEqual(type(self.city.state_id), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "Not applicable for db")
    def test_save_method(self):
        """Test if the save method works"""
        self.city.save()
        self.assertNotEqual(self.city.created_at, self.city.updated_at)

    def test_to_dict_method(self):
        """Test if the to_dict method works"""
        city_dict = self.city.to_dict()
        self.assertEqual(self.city.__class__.__name__, 'City')
        self.assertIsInstance(city_dict['created_at'], str)
        self.assertIsInstance(city_dict['updated_at'], str)


if __name__ == "__main__":
    unittest.main()
