import os
import pymongo
from dotenv import load_dotenv


load_dotenv()

MONGO_CONN_STRING = os.environ['MONGO_CONN_STRING']

def get_mongo_client(conn_string):
    client = pymongo.MongoClient(conn_string)
    db = client.admin
    return db

def generate_mongo_collection(collection_name):
    connection_string = MONGO_CONN_STRING
    db = get_mongo_client(connection_string)
    collection = db[collection_name]
    return collection