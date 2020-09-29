import pymongo
import os


class Database:
    URI = os.environ.get("MONGODB_URL")
    DATABASE = pymongo.MongoClient(URI).get_default_database()

    @staticmethod
    def insert(collection, item):
        Database.DATABASE[collection].insert(item)

    @staticmethod
    def remove(collection, _id):
        Database.DATABASE[collection].remove(_id)

    @staticmethod
    def update(collection, query, item):
        Database.DATABASE[collection].update(spec=query, document={"$set": item})

    @staticmethod
    def find_one_by(collection, query):
        return Database.DATABASE[collection].find_one(query)
