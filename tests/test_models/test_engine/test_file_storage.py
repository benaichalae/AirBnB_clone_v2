#!/usr/bin/python3
"""Module for testing file storage"""
import unittest
import os
from models.base_model import BaseModel
from models import storage


class TestFileStorage(unittest.TestCase):
    """Test class for the FileStorage module"""

    def setUp(self):
        """Set up the test environment."""
        # Clear the storage objects for a clean slate in each test
        del_list = list(storage.all().keys())
        for key in del_list:
            del storage.all()[key]

    def tearDown(self):
        """Remove the storage file at the end of tests."""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_objects_list_empty(self):
        """Test if __objects is initially empty."""
        self.assertEqual(len(storage.all()), 0)

    def test_new_object_added(self):
        """Test if a new object is correctly added to __objects."""
        new_instance = BaseModel()
        for obj in storage.all().values():
            temp_obj = obj
        self.assertTrue(temp_obj is new_instance)

    def test_all_method(self):
        """Test if the all() method properly returns __objects."""
        new_instance = BaseModel()
        objects_dict = storage.all()
        self.assertIsInstance(objects_dict, dict)

    def test_base_model_instantiation(self):
        """Test if a file is not created on BaseModel save."""
        new_instance = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty_data_saved_to_file(self):
        """Test if data is saved to the file."""
        new_instance = BaseModel()
        data = new_instance.to_dict()
        new_instance.save()
        loaded_instance = BaseModel(**data)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save_method(self):
        """Test the save() method of FileStorage."""
        new_instance = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload_method(self):
        """Test if the reload() method successfully loads the storage file to __objects."""
        new_instance = BaseModel()
        storage.save()
        storage.reload()
        loaded_instance = storage.all().popitem()[1]
        self.assertEqual(new_instance.to_dict()['id'], loaded_instance.to_dict()['id'])

    def test_reload_from_empty_file(self):
        """Test if reloading from an empty file raises a ValueError."""
        with open('file.json', 'w') as file:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent_file(self):
        """Test if nothing happens when reloading from a nonexistent file."""
        self.assertEqual(storage.reload(), None)

    def test_base_model_save_method(self):
        """Test if the BaseModel save method calls storage save."""
        new_instance = BaseModel()
        new_instance.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_file_path_type(self):
        """Test if __file_path is a string."""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_objects_type(self):
        """Test if __objects is a dictionary."""
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """Test if the key is properly formatted."""
        new_instance = BaseModel()
        instance_id = new_instance.to_dict()['id']
        key = storage.all().popitem()[0]
        self.assertEqual(key, f"{new_instance.__class__.__name__}.{instance_id}")

    def test_storage_var_created(self):
        """Test if the FileStorage object storage is created."""
        from models.engine.file_storage import FileStorage
        self.assertIsInstance(storage, FileStorage)


if __name__ == '__main__':
    unittest.main()

