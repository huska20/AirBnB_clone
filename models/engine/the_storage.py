#!/usr/bin/python3
"""
    FileStorage class definition
"""
import json
import models


class FileStorage:
    """Serializes and deserializes instances to/from JSON"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        json_dict = {}
        for key, obj in self.__objects.items():
            json_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(json_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                json_dict = json.load(file)
                for key, value in json_dict.items():
                    class_name = key.split('.')[0]
                    obj = models.classes[class_name](**value)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass
