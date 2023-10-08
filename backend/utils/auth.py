import os
from jose import jwt
from typing import Union
from datetime import datetime, timedelta
from passlib.context import CryptContext
from models.auth import UserInDB
from dotenv import load_dotenv
from models.serializers import UserListSerializer

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

  filter = {
    "username": username
  }

  user = users_db_col.find_one(filter)
  if user is not None:
      user_dict = user
      return UserInDB(**user_dict)

def get_all_users(mongo_client):
  db = mongo_client["chatrDB"]
  users_db_col = db["users_db"]

  # since we need all users so filter is empty dict
  filter = {}
  all_users_list = UserListSerializer(users_db_col.find(filter))

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