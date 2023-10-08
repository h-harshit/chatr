import os
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, HTTPException, status, Depends
from utils.auth import get_user
from models.auth import User, TokenData
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

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRES_MINUTES"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Could not validate credentials",
    headers = {"WWW-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception
  
  user = get_user(mongo_client, username = token_data.username)
  if user is None:
    raise credentials_exception
  return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
  if current_user.disabled == "true":
    raise HTTPException(status_code=400, detail = "Inactive User")
  return current_user

async def get_user_role(current_user: User = Depends(get_current_user)):
  return current_user.role


