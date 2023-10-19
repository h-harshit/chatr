from models.groups import Group
from models.msg import Message
from models.serializers import GroupSerializer, GroupListSerializer
from pymongo.collection import ReturnDocument
from fastapi import status, HTTPException
from bson.objectid import ObjectId

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

def update_group_members_in_mongo(mongo_client, group_id, username, payload):
  db = mongo_client["chatrDB"]
  group_db_col = db["group_db"]

  group_admin = group_db_col.find_one({'group_id': group_id}, projection=["group_admin"])
  if username in group_admin['group_admin']:
    updated_group = group_db_col.find_one_and_update(
      {'group_id': group_id}, {'$set': payload}, return_document=ReturnDocument.AFTER)
    return updated_group
  else:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "Only Group Admin can add/delete users",
      headers = {"WWW-Authenticate": "Bearer"}
    )

def like_msg_mongo(mongo_client, group_id:str, msg_id:str, username:str):
  db = mongo_client["chatrDB"]
  group_msg_col = db["group_msg"]
  likes_in_msg = group_msg_col.find_one({'_id': ObjectId(msg_id)})['likes']
  if username in likes_in_msg:
    raise HTTPException(
      status_code = status.HTTP_409_CONFLICT,
      detail = "User has already liked the message"
    )
  else:
    liked_msg = group_msg_col.find_one_and_update({'_id': ObjectId(msg_id)}, {'$push': {'likes': username}}, return_document=ReturnDocument.AFTER)
    return liked_msg




