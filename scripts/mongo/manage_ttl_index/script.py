import sys
from typing import Collection
from pymongo.collection import Collection
import pymongo

from scripts.mongo.config import generate_mongo_collection

WEEKS_TO_KEEP = 2
TTL_SECONDS = WEEKS_TO_KEEP * 7 * 24 * 60 * 60

DEFAULT_COLLECTION = 'states'

VALID_FUNCS = [
    'create',
    'delete'
]


def create_index(collection, ttl_seconds_lifespan):
    print(f"Creating TTL index on {collection.full_name} collection for {ttl_seconds_lifespan} seconds")

    res = collection.create_index([("_ts", pymongo.ASCENDING)], expireAfterSeconds=ttl_seconds_lifespan, background=True)

    print(f"CREATED INDEX {res}")


def delete_index(collection):
    print(f"Deleting TTL index on {collection.full_name} collection")

    collection.drop_index('_ts_1')

    print(f"DELETED INDEX _ts_1")


def run(func, collection, ttl_seconds_lifespan):

    if func == 'create':
        create_index(collection, ttl_seconds_lifespan)
    else:
        delete_index(collection)


try:
    collection_name = sys.argv[1]
except:
    print(f"No/invalid collection supplied, defaulting to {DEFAULT_COLLECTION}")
    collection_name = DEFAULT_COLLECTION

try:
    func_name = sys.argv[2]
    if func_name not in VALID_FUNCS:
        raise Exception(f"{func_name} is not a valid function")
except:
    print(f"No/invalid function supplied (valid functions are {VALID_FUNCS})")
    exit()

mongo_collection: Collection = generate_mongo_collection(collection_name)

run(func_name, mongo_collection, TTL_SECONDS)