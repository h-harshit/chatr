import os
import json
from datetime import datetime, timedelta

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from utils.socket import SocketConnection


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from utils.msg import  write_group_msg

from routers import auth, groups, admin
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


uri = os.environ["MONGO_URI"]
mongo_client = MongoClient(uri, server_api=ServerApi('1'))

try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(groups.router)



@app.get("/")
async def home():
  return {"home":"chatr"}

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

socket_conn_manager = SocketConnection()

@app.websocket("/ws/{group_id}/{client_id}")
async def ws_endp(websocket: WebSocket, group_id:str, client_id: int) -> None:
  await socket_conn_manager.connect(websocket, client_id)
  try:
    while True:
      data = await websocket.receive_text()
      print(f"Msg: {data}")
      timestamp = datetime.now()
      msg_info = {
        'member': client_id,
        'msg_body': data
      }

      broadCastDataObj = {
        'member': client_id,
        'msg_body': data,
        'group_id': group_id,
        'timestamp':str(timestamp)
      }
      await socket_conn_manager.broadcast(json.dumps(broadCastDataObj), websocket, client_id)
      write_group_msg(mongo_client, group_id, msg_info, timestamp)
  except WebSocketDisconnect as disconnect_err:
    socket_conn_manager.disconnect(websocket, client_id)
    print("error",disconnect_err)

