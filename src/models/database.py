import pymongo

__author__ = 'jamie'



class Database(object):

    DATABASE = None

    @staticmethod
    def initialize(uri):
        client = pymongo.MongoClient(uri)
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def find(collection, query, sort=None, direction=1, limit=None):
        if collection is not None:
            if sort:
                cursor = Database.DATABASE[collection].find(query).sort(sort, direction)
            else:
                cursor = Database.DATABASE[collection].find(query)

            if limit:
                return cursor.limit(limit)
            else:
                return cursor
        else:
            raise pymongo.errors.InvalidOperation

    @staticmethod
    def find_one(collection, query):
        if collection is not None:
            return Database.DATABASE[collection].find_one(query)
        else:
            raise pymongo.errors.InvalidOperation

    @staticmethod
    def insert(collection, data):
        if collection is not None:
            return Database.DATABASE[collection].insert(data)
        else:
            raise pymongo.errors.InvalidOperation

    @staticmethod
    def update(collection, query, data, upsert=False):
        if collection is not None:
            return Database.DATABASE[collection].update(query, data, upsert=upsert)
        else:
            raise pymongo.errors.InvalidOperation

    @staticmethod
    def remove(collection, query):
        if collection is not None:
            return Database.DATABASE[collection].remove(query)
        else:
            raise pymongo.errors.InvalidOperation