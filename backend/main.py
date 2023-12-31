import os
import json
from datetime import datetime, timedelta

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from utils.socket import SocketConnection

from utils.msg import  write_group_msg
from routers import auth, groups, admin

from database import mongo_client

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(admin.router, prefix="/api/admin")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(groups.router, prefix="/api/groups")


@app.get("/")
async def home():
  return {"home":"chatr"}


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

