from pydantic import BaseModel
from typing import List
from datetime import datetime
from bson.objectid import ObjectId

class Message(BaseModel):
  member: str
  msg: str
  group_id: str
  timestamp: datetime
  likes: List[str]

  class Config:
    from_attributes = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

