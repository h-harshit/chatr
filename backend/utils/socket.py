from typing import List, Dict
from fastapi import WebSocket


class BaseSocketConnection():
  def __init__(self) -> None:
    self.active_conn_dict: Dict[int, WebSocket] = dict()
  
  async def connect(self, websocket: WebSocket, client_id) -> None:
    await websocket.accept()
    self.active_conn_dict[client_id] = websocket
      

  def disconnect(self, websocket: WebSocket, client_id) -> None:
    del self.active_conn_dict[client_id]


class SocketConnection(BaseSocketConnection):
  def __init__(self) -> None:
    super().__init__()
  
  async def message(self, msg: str, websocket: WebSocket) -> None:
    await websocket.send_text(msg)

  async def broadcast(self, broadCastObj: dict, websocket: WebSocket, sender_id) -> None:
    print("num conn: ", len(self.active_conn_dict.keys()))
    print(self.active_conn_dict)
    for client_id in self.active_conn_dict:
      conn = self.active_conn_dict[client_id]
      await conn.send_text(broadCastObj)

