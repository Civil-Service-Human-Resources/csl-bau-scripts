import sys
from typing import Collection
from pymongo.collection import Collection
import pymongo

from scripts.mongo.config import generate_mongo_collection

DEFAULT_WEEKS_TO_KEEP = 2

DEFAULT_COLLECTION = 'states'

VALID_FUNCS = [
    'create',
    'delete'
]


def create_index(collection, ttl_seconds_lifespan):
    print(f"Creating TTL index on {collection.full_name} collection for {ttl_seconds_lifespan} seconds")

    res = collection.create_index([("_ts", pymongo.ASCENDING)], expireAfterSeconds=ttl_seconds_lifespan, background=True)

    print(f"CREATED COLLECTION {res}")


def delete_index(collection):
    print(f"Deleting TTL index on {collection.full_name} collection")

    collection.drop_index('_ts_1')

    print(f"DELETED INDEX _ts_1")


def run():

    try:
        collection_name = sys.argv[1]
    except:
        print(f"No/invalid collection supplied")
        exit()

    try:
        func_name = sys.argv[2]
        if func_name not in VALID_FUNCS:
            raise Exception(f"{func_name} is not a valid function")
    except:
        print(f"No/invalid function supplied (valid functions are {VALID_FUNCS})")
        exit()

    try:
        weeks_to_keep = int(sys.argv[3])
        ttl_seconds = weeks_to_keep * 7 * 24 * 60 * 60
    except:
        print(f"No/invalid weeks to keep supplied (number of weeks to retain data before it is deleted)")
        exit()

    mongo_collection: Collection = generate_mongo_collection(collection_name)

    if func_name == 'create':
        create_index(mongo_collection, ttl_seconds)
    else:
        delete_index(mongo_collection)


run()