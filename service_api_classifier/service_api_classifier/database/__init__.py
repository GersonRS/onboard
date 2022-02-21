import os
from pymongo import MongoClient

CONNECTION_STRING = (
    "mongodb://"
    + os.environ.get("MONGODB_USERNAME", "admin")
    + ":"
    + os.environ.get("MONGODB_PASSWORD", "admin")
    + "@"
    + os.environ.get("MONGODB_HOSTNAME", "localhost")
    + ":27017"
)
COLLECTION = os.environ.get("MONGODB_DATABASE", "onboard-classifier")

__db = None


def get_database():
    global __db
    if __db is None:
        __db = MongoClient(CONNECTION_STRING)
    return __db[COLLECTION.strip()]
