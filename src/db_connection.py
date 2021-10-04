from settings import config
from pymongo import MongoClient


def get_db():
    client = MongoClient(config['MONGO_CONNECTION_STRING'])
    return client[config['MONGO_DB']]
