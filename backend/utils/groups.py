from models.groups import Group
from models.msg import Message
from models.serializers import GroupSerializer, GroupListSerializer

def get_group_info(mongo_client, group_id):
  db = mongo_client["chatrDB"]
  group_db_col = db["group_db"]

  query_filter = {"group_id": group_id}

  group_dict = group_db_col.find_one(query_filter)
  group_dict = GroupSerializer(group_dict)
  return Group(**group_dict)

def get_group_messages(mongo_client, group_id):
  db = mongo_client["chatrDB"]
  group_msg_db = db["group_msg"]

  query_filter = {"group_id": group_id}

  group_messages = [group_msg for group_msg in group_msg_db.find(query_filter)]
  group_message_list = [Message(**grp_msg) for grp_msg in group_messages]
  return group_messages

def create_group_mongo(mongo_client,group: Group):
  db = mongo_client["chatrDB"]
  group_db_col = db["group_db"]

  group_body = {
    'group_id': group.group_id,
    'group_name': group.group_name,
    'group_members': group.group_members,
    'group_admin': group.group_admin
  }

  group_db_col.insert_one(group_body)
  # del group_body["_id"]
  return {"status":"success", "group": group_body}

def get_groups_list_mongo(mongo_client, username):
  db = mongo_client["chatrDB"]
  group_db_col = db["group_db"]

  query_filter = {'group_members':{'$in':[username]}}

  group_list = GroupListSerializer(group_db_col.find(query_filter))
  
  return group_list

