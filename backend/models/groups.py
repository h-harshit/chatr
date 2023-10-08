from pydantic import BaseModel
from typing import List
from models.msg import Message
from models.auth import User
from bson.objectid import ObjectId

class Group(BaseModel):
  group_id: str
  group_name: str
  group_members: List[str]
  group_admin: List[str]

  class Config:
    orm_mode = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class GroupData(BaseModel):
  group_info: Group
  group_messages: List[Message]