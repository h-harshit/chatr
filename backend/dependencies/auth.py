from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, HTTPException, status, Depends
from .utils.auth import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "20f33a0423634a009683a2ed0a609bae3042b774cd2ff0232cc015a34bcb509a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": "false",
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": "true",
    },
}

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
  
  user = get_user(fake_users_db, username = token_data.username)
  if user is None:
    raise credentials_exception
  return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
  if current_user.disabled == "true":
    raise HTTPException(status_code=400, detail = "Inactive User")
  return current_user
