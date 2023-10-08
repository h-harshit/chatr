import os
from jose import jwt
from typing import Union
from datetime import datetime, timedelta
from passlib.context import CryptContext
from models.auth import UserInDB
from dotenv import load_dotenv
from models.auth import User
from fastapi import HTTPException, status
from pymongo.collection import ReturnDocument

load_dotenv()

# secure secret key generated using openssl
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRES_MINUTES"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return pwd_context.hash(password)

def get_user(mongo_client, username: str):
  db = mongo_client["chatrDB"]
  users_db_col = db["users_db"]

  query_filter = {
    "username": username
  }

  user = users_db_col.find_one(query_filter)
  if user is not None:
      user_dict = user
      return UserInDB(**user_dict)

def get_all_users(mongo_client):
  # avoid circular imports
  from models.serializers import  UserListSerializer
  db = mongo_client["chatrDB"]
  users_db_col = db["users_db"]

  # since we need all users so filter is empty dict
  query_filter = {}
  all_users_list = UserListSerializer(users_db_col.find(query_filter))

  return all_users_list


def authenticate_user(mongo_client, username:str, password:str):
  user = get_user(mongo_client, username)
  if not user:
    return False
  if not verify_password(password, user.password):
    return False
  return user

def create_access_token(data:dict, expires_delta: Union[timedelta, None] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
  return encoded_jwt

def insert_user_to_db(mongo_client, user: User):
  # avoiding circular imports
  from models.serializers import  UserSerializer, NewUserSerializer
  db = mongo_client["chatrDB"]
  users_db_col = db["users_db"]

  created_at = datetime.now()
  dict_user = dict(user)

  user_in_db = get_user(mongo_client, dict_user["username"])
  if user_in_db is None:
    new_user = NewUserSerializer(dict_user)

    users_db_col.insert_one(new_user)

    created_user = UserSerializer(new_user)
    return created_user
  
  else:
    raise HTTPException(
      status_code = status.HTTP_409_CONFLICT,
      detail = "User Already Exists",
      headers = {"WWW-Authenticate": "Bearer"}
    )
  
def update_user_in_db(mongo_client, username, payload:dict):
  # avoiding circular imports
  from models.serializers import  UserSerializer
  db = mongo_client["chatrDB"]
  users_db_col = db["users_db"]

  updated_at = datetime.now()
  payload["updated_at"] = updated_at

  updated_user = users_db_col.find_one_and_update(
    {'username': username}, {'$set': payload}, return_document=ReturnDocument.AFTER)

  if not updated_user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'No user with this username: {username} found'
      )
  else:
    updated_user = UserSerializer(updated_user)
    return updated_user
