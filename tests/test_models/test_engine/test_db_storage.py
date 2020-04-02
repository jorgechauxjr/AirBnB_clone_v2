#!/usr/bin/python3
"""test for databasse storage"""
import unittest
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review
from os import getenv
import MySQLdb
import pep8
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from models import storage
import os
import MySQLdb


class TestDataBaseStorage(unittest.TestCase):
    """Test for the Database"""

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "Don´t run if is file storage")
    def test_attributes_DBStorage(self):
        """Test the methods"""

        self.assertTrue(hasattr(DBStorage, 'new'))
        self.assertTrue(hasattr(DBStorage, 'save'))
        self.assertTrue(hasattr(DBStorage, 'all'))
        self.assertTrue(hasattr(DBStorage, 'delete'))
        self.assertTrue(hasattr(DBStorage, 'reload'))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "Don´t run if is file storage")
    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""

        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "Don´t run if is file storage")
    def test_pep8_DataBaseStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

if __name__ == "__main__":
    unittest.main()
