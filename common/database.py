import pymongo


class Database:
    URI = "mongodb://127.0.0.1:27017/covInd"
    DATABASE = pymongo.MongoClient(URI).get_database()

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


