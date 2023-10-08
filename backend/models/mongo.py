from pydantic import BaseModel

class Group(BaseModel):
  id: str
  name: str
  members: list
  admin: list