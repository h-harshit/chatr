from datetime import datetime

def get_group_msg_data(mongo_client, group_id):
  db = mongo_client["chatrDB"]
  group_msg_col = db["group_msg"]
  group_msg_data = [msg for msg in group_msg_col.find({'group_id': group_id}).sort('timestamp',-1)]
  final_group_msg_data = []
  for group_msg in group_msg_data:
    msg_obj = {}
    msg_obj['group_id'] = group_msg['group_id']
    msg_obj['timestamp'] = str(group_msg['timestamp'])
    msg_obj['member'] = group_msg['msg_info']['member']
    msg_obj['msg_body'] = group_msg['msg_info']['msg_body']
    final_group_msg_data.append(msg_obj)
  return final_group_msg_data

def write_group_msg(mongo_client, group_id, msg_info, timestamp):
  db = mongo_client["chatrDB"]
  group_msg_col = db["group_msg"]

  msg_body = {
    'group_id': group_id,
    'timestamp': timestamp,
    'msg_info': msg_info
  }

  group_msg_col.insert_one(msg_body)
