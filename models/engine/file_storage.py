#!/usr/bin/python3
import json
import os
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping class names to their corresponding class objects
CLASSES = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Manages the serialization and deserialization
    of instances to and from a JSON file."""

    def __init__(self):
        """Initialize the FileStorage instance."""
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self, cls=None):
        """Retrieve all stored instances or filtered instances by class."""
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            return {k: v for k, v in self.__objects.items(
                ) if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Add a new instance to the storage."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serialize instances to the JSON file."""
        json_objects = {key: obj.to_dict(
            ) for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(json_objects, file)

    def reload(self):
        """Deserialize the JSON file to instances."""
        try:
            with open(self.__file_path, 'r') as file:
                json_objects = json.load(file)
            for key, obj_dict in json_objects.items():
                class_name = obj_dict["__class__"]
                if class_name in CLASSES:
                    obj = CLASSES[class_name](**obj_dict)
                    self.__objects[key] = obj
        except Exception as FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Remove an instance from storage if it exists."""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects.pop(key, None)

    def close(self):
        """Deserialize the JSON file to instances before exiting."""
        self.reload()
