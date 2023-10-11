from fastapi.testclient import TestClient
from main import app
from routers.test_auth import login

client = TestClient(app)

def is_current_user_admin():
  auth_response, auth_token = login()
  assert auth_response.status_code == 200
  headers = {
    "Authorization": f"Bearer {auth_token}"
  }
  response = client.get("api/auth/users/me", headers=headers)
  role = response.json()["role"]
  return role, headers

def test_create_users():
  is_admin, headers = is_current_user_admin()
  assert is_admin == "admin"
  data = {
    "username": "testuser3",
    "email": "test3@user.com",
    "full_name": "test3",
    "disabled": "false",
    "role": "user",
    "password": "testpassword3"
  }
  response = client.post("/api/admin/users/create", data=data, headers=headers)
  assert response.status_code == 200
  assert response.json()["status"] == "success"

def test_edit_users():
  is_admin, headers = is_current_user_admin()
  assert is_admin == "admin"
  payload = {"email": "test-1@user.com"}
  user = "test"
  response = client.patch(f"/api/admin/users/edit/{user}", data=payload, headers=headers)
  assert response.status_code == 200
  assert response.json()["status"] == "success"

