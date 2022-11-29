from mysql import connector
from scripts.script_config import get_sql_conn
import os
import json

from datetime import datetime
from datetime import timezone
from scripts.mongo.config import generate_mongo_collection
cnx = connector.connect(**get_sql_conn("learner_record"))

def find_records_sql():
	return "select module_id from module_record where state = 'IN_PROGRESS' and completion_date < '2022-11-25' and completion_date > '2022-11-01'"

def update_records_sql(module_id, users):
	user_ids_in = ",".join([f"'{user_id}'" for user_id in users])
	return f"update module_record set state = 'COMPLETED' where module_id = '{module_id}' and user_id in ({user_ids_in}) and state = 'IN_PROGRESS'"
	

def generate_query(module_id):
	from_date = datetime(2022, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
	to_date = datetime(2022, 11, 25, 0, 0, 0, tzinfo=timezone.utc)
	return {
		"statement.object.id": f"http://cslearning.gov.uk/modules/{module_id}",
		"statement.verb.id": "http://adlnet.gov/expapi/verbs/completed",
		"timestamp": {"$gt": from_date, "$lt": to_date}
	}

def run():

	cursor = cnx.cursor()
	cursor.execute(find_records_sql())
	module_id_rows = cursor.fetchall()

	module_ids = [row[0] for row in module_id_rows]
	updates = {}
	mongo = generate_mongo_collection('statements')
	print(f"{len(module_ids)} modules found that might need updates")
	for module_id in module_ids:
		query = generate_query(module_id)
		count = mongo.count_documents(query)
		if count:
			updates[module_id] = [statement['statement']['actor']['account']['name'] for statement in mongo.find(query)]
	with open(os.path.dirname(__file__) + '/results.json', 'w') as file:
		file.write(json.dumps(updates))

	print(f"{len(updates.keys())} modules to update")

	if len(updates.keys()):

		sql_updates = ""

		for module_id in updates.keys():
			users = updates[module_id]
			sql = update_records_sql(module_id, users)
			print(f"executing SQL for module {module_id} and {len(users)} users")
			sql_updates += f"{sql}\n\n"
			cursor = cnx.cursor()
			cursor.execute(sql)
		cnx.commit()

		with open(os.path.dirname(__file__) + '/sql.txt', 'w') as file:
			file.write(sql_updates)


run()