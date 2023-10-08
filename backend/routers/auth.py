import os
from datetime import timedelta
from models.auth import Token, User, ListUser
from fastapi import APIRouter, HTTPException, status, Depends
from utils.auth import authenticate_user, create_access_token, get_all_users
from fastapi.security import  OAuth2PasswordRequestForm
from dependencies.auth import get_current_active_user
from dotenv import load_dotenv
from typing import List
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.environ["MONGO_URI"]
mongo_client = MongoClient(uri, server_api=ServerApi('1'))

try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


ACCESS_TOKEN_EXPIRES_MINUTES=int(os.environ['ACCESS_TOKEN_EXPIRES_MINUTES'])

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  user = authenticate_user(mongo_client, form_data.username, form_data.password)
  if not user:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "Incorrect username or password",
      headers = {"WWW-Authenticate": "Bearer"}
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
  access_token = create_access_token(
    data={"sub":user.username}, expires_delta = access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
  return current_user

@router.get("/users/all", response_model=ListUser)
async def read_all_users(current_user:User = Depends(get_current_active_user)):
  if current_user:
    all_users = get_all_users(mongo_client)
    return {'users': all_users}
  else:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "UnAuthorized User",
      headers = {"WWW-Authenticate": "Bearer"}
    )
