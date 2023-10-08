from pydantic import BaseModel
from typing import Union, List
from datetime import datetime
from bson.objectid import ObjectId

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: Union[str, None] = None

class User(BaseModel):
  username: str
  email: Union[str, None] = None
  full_name: Union[str, None] = None
  disabled: Union[str, None] = None
  role: str
  created_at: datetime = datetime.now() 
  updated_at: Union[datetime, None] = None
  deleted_at: Union[datetime, None] = None

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

class UserInDB(User):
  password: str

class ListUser(BaseModel):
  users: List[User]

class CreatedUser(BaseModel):
  status: str
  created_user: User

class UpdateUser(BaseModel):
  email: Union[str, None] = None
  full_name: Union[str, None] = None
  role: Union[str, None] = None

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class PatchedUser(BaseModel):
  status: str
  updated_user: User
