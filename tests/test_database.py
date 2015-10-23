from unittest import TestCase
from database import Database
from src.app import setup_database

__author__ = 'jamie'

class TestDatabase (TestCase):

    @classmethod
    def setUpClass(cls):
        setup_database()

    def test_collection_add(self):
        collection = "test"
        data = {"user": "test"}
        Database.insert(collection, data)

        self.assertTrue(Database.find_one(collection, data))
