#!/usr/bin/python3
"""Unit tests for the State class"""

import unittest
import os
from models.state import State
from models.base_model import BaseModel
import pep8


class TestState(unittest.TestCase):
    """Test cases for the State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.state = State()
        cls.state.name = "CA"

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.state

    def tearDown(self):
        """Tear down after each test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_compliance(self):
        """Check if the code complies with pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0, "Fix pep8 issues")

    def test_docstring_presence(self):
        """Check if docstrings are present"""
        self.assertIsNotNone(State.__doc__)

    def test_attributes_existence(self):
        """Check if State class has required attributes"""
        attributes = ['id', 'created_at', 'updated_at', 'name']
        for attribute in attributes:
            self.assertTrue(attribute in self.state.__dict__)

    def test_is_subclass_of_base_model(self):
        """Check if State is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.state.__class__, BaseModel))

    def test_attribute_types(self):
        """Check attribute type for State"""
        self.assertEqual(type(self.state.name), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "Not applicable for db")
    def test_save_method(self):
        """Test if the save method works"""
        self.state.save()
        self.assertNotEqual(self.state.created_at, self.state.updated_at)

    def test_to_dict_method(self):
        """Test if the to_dict method works"""
        state_dict = self.state.to_dict()
        self.assertEqual(self.state.__class__.__name__, 'State')
        self.assertIsInstance(state_dict['created_at'], str)
        self.assertIsInstance(state_dict['updated_at'], str)


if __name__ == "__main__":
    unittest.main()
