def UserSerializer(user) -> dict:
  return {
    "id": str(user["_id"]),
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
