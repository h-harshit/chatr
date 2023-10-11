from fastapi.testclient import TestClient
from main import app
from routers.test_auth import login

client = TestClient(app)

def test_login():
  auth_response, token = login()
  assert auth_response.status_code == 200
  token = auth_response.json()["access_token"]
  assert token is not None

def test_get_group_data():
  auth_response, auth_token = login()
  assert auth_response.status_code == 200
  headers = {
    "Authorization": f"Bearer {auth_token}"
  }
  group_id = 'testuser|Friends'
  response = client.get(f"/api/groups/group_data/{group_id}", headers=headers) 
  assert response.status_code == 200

def test_create_group():
  auth_response, auth_token = login()
  assert auth_response.status_code == 200
  headers = {
    "Authorization": f"Bearer {auth_token}"
  }
  group_data = {
    'group_id': 'testuser1|Family',
    'group_name': 'Family',
    'group_members': ['testuser1', 'testuser2'],
    'group_admin': ['testuser1']
  }

  response = client.post(f"/api/groups/create", data=group_data, headers=headers) 
  assert response.status_code == 200
  assert response.json()["status"] == "success" 

def test_get_groups():
  auth_response, auth_token = login()
  assert auth_response.status_code == 200
  headers = {
    "Authorization": f"Bearer {auth_token}"
  }
  username = "testuser"
  response = client.get(f"/api/groups/{username}", headers=headers)
  assert response.status_code == 200
  assert response.json()["group_list"] == [{"group_id":"testuser|Friends","group_name":"Friends","group_members":["harshit","testuser","neha"],"group_admin":["testuser"]}]

