from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def login():
  auth_response = client.post("/api/auth/login", data={"username": "testuser", "password": "testpassword"})
  token = auth_response.json()["access_token"]
  return auth_response, token

def test_login():
  auth_response, token = login()
  assert auth_response.status_code == 200
  assert token is not None

def test_current_user():
  auth_response, auth_token = login()
  assert auth_response.status_code == 200
  headers = {
    "Authorization": f"Bearer {auth_token}"
  }
  response = client.get("api/auth/users/me", headers=headers)
  assert response.status_code == 200
  assert response.json() == {"username":"testuser","email":"test@user.com","full_name":"test","disabled":"false","role":"admin","created_at":'2023-10-11T16:20:14.769000',"updated_at":'2023-10-11T16:20:14.769000',"deleted_at":None}

def test_get_all_users():
  auth_response, auth_token = login()
  assert auth_response.status_code == 200
  headers = {
    "Authorization": f"Bearer {auth_token}"
  }
  response = client.get("api/auth/users/all", headers=headers)
  assert response.status_code == 200


