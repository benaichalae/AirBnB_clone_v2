#!/usr/bin/python3
"""Unit tests for the Amenity class"""

import unittest
import os
from models.amenity import Amenity
from models.base_model import BaseModel
import pep8


class TestAmenity(unittest.TestCase):
    """Test cases for the Amenity class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.amenity = Amenity()
        cls.amenity.name = "Breakfast"

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.amenity

    def tearDown(self):
        """Tear down after each test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_compliance(self):
        """Check if the code complies with pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0, "Fix pep8 issues")

    def test_docstring_presence(self):
        """Check if docstrings are present"""
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes_existence(self):
        """Check if Amenity class has required attributes"""
        attributes = ['id', 'created_at', 'updated_at', 'name']
        for attribute in attributes:
            self.assertTrue(attribute in self.amenity.__dict__)

    def test_is_subclass_of_base_model(self):
        """Check if Amenity is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.amenity.__class__, BaseModel))

    def test_attribute_types(self):
        """Check attribute types for Amenity class"""
        self.assertEqual(type(self.amenity.name), str)

    def test_save_method(self):
        """Test if the save method works"""
        self.amenity.save()
        self.assertNotEqual(self.amenity.created_at, self.amenity.updated_at)

    def test_to_dict_method(self):
        """Test if the to_dict method works"""
        self.assertTrue('to_dict' in dir(self.amenity))


if __name__ == "__main__":
    unittest.main()
