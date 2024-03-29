# Manage TTL index

This script will create or delete a TTL index against the specified collection in CosmosDB.

The TTL index will actively delete documents that are older than a specified time period. The default value for this is **2 weeks**.

This script was created mainly for use with the `states` collection, as buildup of states on the platform causes exception buildup. 2 weeks is a suitable amount, as most learners will have completed their learning by then, thus there is no risk in deleting bookmarks (state data) after this timeframe.

## Rquirements

- Python > 3.7
- .env file with `MONGO_CONN_STRING` set. This can be found within the Azure CosmosDB connection string blade.

## Usage

Run the script with the `run.sh` command in the root directory, followed by:

`scripts/mongo/manage_ttl_index_script.py <COLLECTION_NAME> <FUNCTION> <WEEKS_TTL>`

Where:

- `<COLLECTION_NAME>` is the name of the mongo collection to apply the index to.
- `<FUNCTION>` `create` or `delete`, depending on the requirement
- `<WEEKS_TTL>` number of weeks for TTL (weeks to keep the data for before deleting it)
