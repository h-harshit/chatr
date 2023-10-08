def create_group_mongo(mongo_client,group_id, group_name, group_members, group_admin):
  db = mongo_client["chatrDB"]
  group_db_col = db["group_db"]

  group_body = {
    'group_id': group_id,
    'group_name': group_name,
    'group_members': group_members,
    'group_admin': group_admin
  }

  group_db_col.insert_one(group_body)
  del group_body["_id"]
  return {"status":"success", "group_body": group_body}

def get_groups_list_mongo(mongo_client, client_id):
  db = mongo_client["chatrDB"]
  group_db_col = db["group_db"]

  filter = {'group_members':{'$in':[str(client_id)]}}

  group_list = [elem for elem in group_db_col.find(filter)]
  for group in group_list:
    del group["_id"]
  
  return group_list

