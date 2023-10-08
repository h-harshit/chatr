import os
from fastapi import APIRouter, Depends, status, HTTPException
from models.auth import User, UserInDB, CreatedUser
from dependencies.auth import get_user_role
from utils.auth import insert_user_to_db
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

uri = os.environ["MONGO_URI"]
mongo_client = MongoClient(uri, server_api=ServerApi('1'))

try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

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

