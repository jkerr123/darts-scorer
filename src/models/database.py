import pymongo

__author__ = 'jamie'

MONGODB_URI = 'mongodb://heroku_plq17kjt:au06mdnk5ll4tq8dudvfccu89d@ds041934.mongolab.com:41934/heroku_plq17kjt'


class Database(object):

    DATABASE = None

    @staticmethod
    def initialize(database):
        client = pymongo.MongoClient(MONGODB_URI)
        Database.DATABASE = client[database]

