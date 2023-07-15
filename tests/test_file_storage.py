import unittest
import os
import json
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.storage = FileStorage()
        self.file_path = "file.json"

    def tearDown(self):
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_all(self):
        all_objects = self.storage.all()
        self.assertEqual(all_objects, {})

        state = State()
        state.id = "123"
        state.name = "California"
        self.storage.new(state)

        city = City()
        city.id = "456"
        city.name = "Los Angeles"
        self.storage.new(city)

        all_objects = self.storage.all()
        self.assertEqual(len(all_objects), 2)
        self.assertIn("State.123", all_objects)
        self.assertIn("City.456", all_objects)

    def test_new(self):
        state = State()
        state.id = "123"
        state.name = "California"
        self.storage.new(state)

        all_objects = self.storage.all()
        self.assertEqual(len(all_objects), 1)
        self.assertIn("State.123", all_objects)

    def test_save_reload(self):
        state = State()
        state.id = "123"
        state.name = "California"
        self.storage.new(state)

        city = City()
        city.id = "456"
        city.name = "Los Angeles"
        self.storage.new(city)

        self.storage.save()

        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, 'r') as file:
            saved_data = json.load(file)

        self.assertIn("State.123", saved_data)
        self.assertIn("City.456", saved_data)

        new_storage = FileStorage()
        new_storage.reload()

        all_objects = new_storage.all()
        self.assertEqual(len(all_objects), 2)
        self.assertIn("State.123", all_objects)
        self.assertIn("City.456", all_objects)


if __name__ == "__main__":
    unittest.main()
