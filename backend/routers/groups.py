import os
from fastapi import APIRouter, Depends, status, HTTPException
from utils.groups import create_group_mongo, get_groups_list_mongo, get_group_info, get_group_messages
from utils.msg import get_group_msg_data
from models.groups import Group, GroupData
from models.auth import User
from models.msg import Message
from database import mongo_client
from dependencies.auth import get_current_active_user

router = APIRouter()

@router.get("/group_data/{group_id}", response_model=GroupData)
async def get_group_data(group_id, current_user: User = Depends(get_current_active_user)):
  if current_user:
    group_info = get_group_info(mongo_client, group_id)
    group_msg = get_group_messages(mongo_client, group_id)
    return {'group_info':group_info, 'group_messages': group_msg}
  else:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "UnAuthorized User",
      headers = {"WWW-Authenticate": "Bearer"}
    )

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