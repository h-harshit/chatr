from fastapi import APIRouter
from .utils.groups import create_group_mongo, get_groups_list_mongo
from .utils.msg import get_group_msg_data
from .models.mongo import Group

router = APIRouter()

@router.get("/group_data/{group_id}")
async def get_group_msg(group_id):
  print(group_id)
  try:
    group_members = GROUPS[group_id]
  except KeyError:
    group_members = []
  group_msg = get_group_msg_data(mongo_client, group_id)

  return ({'group_members':group_members, 'group_msg': group_msg})

@router.post("/groups/create")
async def create_group(group: Group):
  group_id = group.id
  group_name = group.name
  group_members = group.members
  group_admin = group.admin

  res = create_group_mongo(mongo_client,group_id,group_name, group_members, group_admin)
  return res

@router.get("/groups/{client_id}")
async def get_groups_list(client_id:int):
  res = get_groups_list_mongo(mongo_client, client_id)
  return res