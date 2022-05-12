import sys
from typing import Collection
from pymongo.collection import Collection
import pymongo

from scripts.mongo.config import generate_mongo_collection

WEEKS_TO_KEEP = 2
TTL_SECONDS = WEEKS_TO_KEEP * 7 * 24 * 60 * 60

DEFAULT_COLLECTION = 'states'

def run(collection, ttl_seconds_lifespan):

    print(f"Creating TTL index on {mongo_collection.full_name} collection for {ttl_seconds_lifespan} seconds")

    res = collection.create_index([("_ts", pymongo.ASCENDING)], expireAfterSeconds=ttl_seconds_lifespan, background=True)

    print(f"CREATED COLLECTION {res}")

try:
    collection_name = sys.argv[1]
except:
    print(f"No/invalid collection supplied, defaulting to {DEFAULT_COLLECTION}")
    collection_name = DEFAULT_COLLECTION

mongo_collection: Collection = generate_mongo_collection(collection_name)

run(mongo_collection, TTL_SECONDS)