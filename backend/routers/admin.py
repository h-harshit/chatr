import os
from fastapi import APIRouter, Depends, status, HTTPException
from models.auth import User, UserInDB, CreatedUser, UpdateUser, PatchedUser
from dependencies.auth import get_user_role
from utils.auth import insert_user_to_db, update_user_in_db
from database import mongo_client

router = APIRouter()

@router.post("/admin/users/create", response_model=CreatedUser)
async def create_users(user: UserInDB, role: str = Depends(get_user_role)):
  if role != "admin":
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "Admin level access required",
      headers = {"WWW-Authenticate": "Bearer"}
    )
  created_user = insert_user_to_db(mongo_client, user)
  return { "status":"success", "created_user": created_user}

@router.patch("/admin/users/edit/{username}", response_model=PatchedUser)
async def edit_users(username, payload: UpdateUser, role: str = Depends(get_user_role)):
  if role != "admin":
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "Admin level access required",
      headers = {"WWW-Authenticate": "Bearer"}
    )
  updated_user = update_user_in_db(mongo_client, username, payload.dict(exclude_none=True))
  return {"status": "success", "updated_user": updated_user}


