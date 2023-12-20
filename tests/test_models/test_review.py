#!/usr/bin/python3
"""Unit tests for the Review class"""

import unittest
import os
from models.review import Review
from models.base_model import BaseModel
import pep8


class TestReview(unittest.TestCase):
    """Test cases for the Review class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.rev = Review()
        cls.rev.place_id = "4321-dcba"
        cls.rev.user_id = "123-bca"
        cls.rev.text = "The strongest in the Galaxy"

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.rev

    def tearDown(self):
        """Tear down after each test"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_compliance(self):
        """Check if the code complies with pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0, "Fix pep8 issues")

    def test_docstring_presence(self):
        """Check if docstrings are present"""
        self.assertIsNotNone(Review.__doc__)

    def test_attributes_existence(self):
        """Check if Review class has required attributes"""
        attributes = ['id', 'created_at', 'updated_at',
                      'place_id', 'user_id', 'text']
        for attribute in attributes:
            self.assertTrue(attribute in self.rev.__dict__)

    def test_is_subclass_of_base_model(self):
        """Check if Review is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.rev.__class__, BaseModel))

    def test_attribute_types(self):
        """Check attribute types for Review class"""
        self.assertEqual(type(self.rev.text), str)
        self.assertEqual(type(self.rev.place_id), str)
        self.assertEqual(type(self.rev.user_id), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "Not applicable for db")
    def test_save_method(self):
        """Test if the save method works"""
        self.rev.save()
        self.assertNotEqual(self.rev.created_at, self.rev.updated_at)

    def test_to_dict_method(self):
        """Test if the to_dict method works"""
        review_dict = self.rev.to_dict()
        self.assertEqual(self.rev.__class__.__name__, 'Review')
        self.assertIsInstance(review_dict['created_at'], str)
        self.assertIsInstance(review_dict['updated_at'], str)


if __name__ == "__main__":
    unittest.main()
