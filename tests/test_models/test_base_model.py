#!/usr/bin/python3
"""Unit tests for the BaseModel class"""

import unittest
import os
from models.base_model import BaseModel
import pep8


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.base_model = BaseModel()
        cls.base_model.name = "Kev"
        cls.base_model.num = 20

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.base_model

    def tearDown(self):
        """Tear down after each test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_compliance(self):
        """Check if the code complies with pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0, "Fix pep8 issues")

    def test_docstring_presence(self):
        """Check if docstrings are present"""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_method_existence(self):
        """Check if BaseModel class has required methods"""
        methods = ['__init__', 'save', 'to_dict']
        for method in methods:
            self.assertTrue(hasattr(BaseModel, method))

    def test_instance_of_base_model(self):
        """Test if the instance is of type BaseModel"""
        self.assertTrue(isinstance(self.base_model, BaseModel))

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "Not applicable for db")
    def test_save_method(self):
        """Test if the save method works"""
        self.base_model.save()
        self.assertNotEqual(self.base_model.created_at,
                            self.base_model.updated_at)

    def test_to_dict_method(self):
        """Test if the to_dict method works"""
        base_model_dict = self.base_model.to_dict()
        self.assertEqual(self.base_model.__class__.__name__, 'BaseModel')
        self.assertIsInstance(base_model_dict['created_at'], str)
        self.assertIsInstance(base_model_dict['updated_at'], str)


if __name__ == "__main__":
    unittest.main()
