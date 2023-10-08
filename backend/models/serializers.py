from datetime import datetime
from utils.auth import get_password_hash


def UserSerializer(user) -> dict:
  return {
    "username": user["username"],
    "email": user["email"],
    "full_name": user["full_name"],
    "disabled": user["disabled"],
    "role": user["role"],
    "created_at": user["created_at"],
    "updated_at": user["updated_at"],
    "deleted_at": user["deleted_at"]
  }

def UserListSerializer(user_list) -> list:
  return [UserSerializer(user) for user in user_list]


def NewUserSerializer(user) -> dict:
  created_at = datetime.now()
  return {
    "username": user["username"],
    "email": user["email"],
    "full_name": user["full_name"],
    "password": get_password_hash(user["password"]),
    "disabled": user["disabled"],
    "role": user["role"],
    "created_at": created_at,
    "updated_at": created_at,
    "deleted_at": None
  }

def GroupSerializer(group) -> dict:
  return {
    "group_id": group["group_id"],
    "group_name": group["group_name"],
    "group_members": group["group_members"],
    "group_admin": group["group_admin"]
  }
