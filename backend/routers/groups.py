import os
from fastapi import APIRouter, Depends, status, HTTPException
from utils.groups import *
from utils.msg import get_group_msg_data
from models.groups import Group, GroupData, GroupCreationStatus, GroupList
from models.auth import User
from models.msg import Message, LikedMessage
from database import mongo_client
from dependencies.auth import get_current_active_user
from models.groups import UpdateGroupMembers, PatchedGroup

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

@router.post("/create", response_model=GroupCreationStatus)
async def create_group(group: Group, current_user: User = Depends(get_current_active_user)):
  if current_user:
    res = create_group_mongo(mongo_client, group)
    return {"status": res["status"], "group": res["group"]}
  else:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "UnAuthorized User",
      headers = {"WWW-Authenticate": "Bearer"}
    )

@router.get("/{username}", response_model=GroupList)
async def get_groups_list(username:str, current_user: User = Depends(get_current_active_user)):
  if current_user:
    group_list = get_groups_list_mongo(mongo_client, username)
    return {"group_list": group_list}
  else:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "UnAuthorized User",
      headers = {"WWW-Authenticate": "Bearer"}
    )

@router.patch("/group/update/{group_id}", response_model=PatchedGroup)
async def update_group_members(group_id: str, payload: UpdateGroupMembers, current_user: User = Depends(get_current_active_user)):
  if current_user:
    username = current_user.username
    updated_group = update_group_members_in_mongo(mongo_client, group_id, username, payload.dict(exclude_none=True))
    response =  {
      "status": "success",
      "updated_group": updated_group
    }
    return PatchedGroup(**response)
  else:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "UnAuthorized User",
      headers = {"WWW-Authenticate": "Bearer"}
    )

@router.post("/group/msg/like/{group_id}/{msg_id}", response_model=LikedMessage)
async def like_msg(
      group_id: str,
      msg_id: str,
      current_user: User = Depends(get_current_active_user)
):
  if current_user:
    username = current_user.username
    liked_msg = like_msg_mongo(mongo_client, group_id, msg_id, username)
    return {
      'status': 'success',
      'liked_msg': liked_msg
    }
  else:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "UnAuthorized User",
      headers = {"WWW-Authenticate": "Bearer"}
    )
