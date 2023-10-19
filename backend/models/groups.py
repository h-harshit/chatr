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
    from_attributes = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class GroupData(BaseModel):
  group_info: Group
  group_messages: List[Message]

class GroupCreationStatus(BaseModel):
  status: str
  group: Group

class GroupList(BaseModel):
  group_list: List[Group]

class UpdateGroupMembers(BaseModel):
  group_members: List[str]

class PatchedGroup(BaseModel):
  status: str
  updated_group: Group
  