#!/usr/bin/python3
"""Unit tests for the User class"""

import unittest
import os
from models.user import User
from models.base_model import BaseModel
import pep8


class TestUser(unittest.TestCase):
    """Test cases for the User class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.user = User()
        cls.user.first_name = "Kevin"
        cls.user.last_name = "Yook"
        cls.user.email = "yook00627@gmail.com"
        cls.user.password = "secret"

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.user

    def tearDown(self):
        """Tear down after each test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_compliance(self):
        """Check if the code complies with pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0, "Fix pep8 issues")

    def test_docstring_presence(self):
        """Check if docstrings are present"""
        self.assertIsNotNone(User.__doc__)

    def test_attributes_existence(self):
        """Check if User class has required attributes"""
        attributes = [
            'id', 'created_at', 'updated_at',
            'email', 'password', 'first_name', 'last_name'
        ]
        for attribute in attributes:
            self.assertTrue(attribute in self.user.__dict__)

    def test_is_subclass_of_base_model(self):
        """Check if User is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.user.__class__, BaseModel))

    def test_attribute_types(self):
        """Check attribute types for User class"""
        self.assertEqual(type(self.user.email), str)
        self.assertEqual(type(self.user.password), str)
        self.assertEqual(type(self.user.first_name), str)
        self.assertEqual(type(self.user.last_name), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "Not applicable for db")
    def test_save_method(self):
        """Test if the save method works"""
        self.user.save()
        self.assertNotEqual(self.user.created_at, self.user.updated_at)

    def test_to_dict_method(self):
        """Test if the to_dict method works"""
        user_dict = self.user.to_dict()
        self.assertEqual(self.user.__class__.__name__, 'User')
        self.assertIsInstance(user_dict['created_at'], str)
        self.assertIsInstance(user_dict['updated_at'], str)


if __name__ == "__main__":
    unittest.main()
