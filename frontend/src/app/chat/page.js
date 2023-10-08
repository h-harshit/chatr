"use client";
import { useEffect, useState } from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { setAllChat } from "@/redux/action";
import dp from "../../assets/dp.jpg";
import undrawChatting from "../../assets/svg/undraw_chatting.svg";
import AddCommentIcon from "@mui/icons-material/AddComment";
import OutlinedInput from "@mui/material/OutlinedInput";
import SendIcon from "@mui/icons-material/Send";

export default function ChatApp() {
  const [message, setMessage] = useState("");
  const [lastMessage, setLastMessage] = useState("");
  const [groupId, setGroupId] = useState();
  const [members, setMembers] = useState();
  // const [allChat, setAllChat] = useState([]);

  const [webSocket, setWebSocket] = useState();

  const [groupList, setGroupList] = useState([]);

  const [newGroupName, setNewGroupName] = useState("");
  const [newGroupMembers, setNewGroupMembers] = useState("");
  const [newGroupAdmin, setNewGroupAdmin] = useState("");

  const allChat = useSelector((state) => state.allChat);
  const dispatch = useDispatch();

  let clientId = localStorage.getItem("client_id");
  const webSocketUrl = `ws://localhost:8000/ws/${groupId}/${clientId}`;

  useEffect(() => {
    if (groupId && clientId) {
      const ws = new WebSocket(webSocketUrl);
      setWebSocket(ws);
    }

    getGroupMessage();

    // while (ws.readyState !== 1) {}
  }, [groupId]);

  useEffect(() => {
    if (!webSocket) return;
    webSocket.onmessage = function (event) {
      console.log(event.data);
      const msg = JSON.parse(event.data);
      setLastMessage(msg);
    };
  }, [webSocket]);

  const appendToMessage = (msg) => {
    let tempAllMessages = Object.assign([], allChat);
    tempAllMessages.push(msg);
    dispatch(setAllChat(tempAllMessages));
  };

  const handleMessageChange = (event) => {
    setMessage(event.target.value);
  };

  const handleSendMessage = (event) => {
    if (webSocket && webSocket.readyState === 1) {
      webSocket.send(message);
      setMessage("");
    } else {
      console.log("hrer");
    }
  };

  const getGroupMessage = () => {
    if (groupId) {
      axios.get(`http://localhost:8000/group_data/${groupId}`).then((res) => {
        console.log(res.data);
        let members = res.data.group_members;
        let messages = res.data.group_msg;

        setMembers(members);
        dispatch(setAllChat(messages));
      });
    }
  };

  const getGroupName = () => {
    if (groupId) {
      let currentGroup = groupList.filter(
        (group) => group["group_id"] === groupId
      );
      let currentGroupName = currentGroup[0]["group_name"];
      return currentGroupName;
    } else {
      return "";
    }
  };

  const getGroupMembers = () => {
    if (groupId) {
      let currentGroup = groupList.filter(
        (group) => group["group_id"] === groupId
      );
      let currentGroupMembers = currentGroup[0]["group_members"];
      return currentGroupMembers;
    } else {
      return [];
    }
  };

  useEffect(() => {
    if (lastMessage !== "") {
      appendToMessage(lastMessage);
    }
  }, [lastMessage]);

  const handleCreateGroup = () => {
    console.log(newGroupMembers);
    console.log(newGroupAdmin);
    let apiPayload = {
      id: `${clientId}_${newGroupName}`,
      name: newGroupName,
      members: newGroupMembers.split(","),
      admin: newGroupAdmin.split(","),
    };
    axios
      .post("http://localhost:8000/groups/create", apiPayload)
      .then((res) => {
        console.log(res.data);
      });
  };

  useEffect(() => {
    axios.get(`http://localhost:8000/groups/${clientId}`).then((res) => {
      setGroupList(res.data);
    });
  }, []);

  return (
    <main>
      <section className="fixed h-screen w-[40%] top-0 left-0">
        <div className="flex flex-row justify-between w-[100%] bg-[#f0f2f5] items-center pl-[15px] pt-[10px] pb-[10px] h-[4rem] border-r border-[rgb(239,232,232)]">
          <div>
            <img
              src={dp.src}
              alt="profile picture"
              className="w-[40px] h-[40px] rounded-full"
            />
          </div>
          <div className="mr-[3rem]">
            <AddCommentIcon />
          </div>
        </div>
        <div className="mt-[1rem]">
          {groupList.map((group, idx) => {
            return (
              <div
                key={idx}
                className="pl-[20px] flex flex-row gap-[2rem] justify-start items-center"
              >
                <div>
                  <img
                    src={dp.src}
                    alt="profile picture"
                    className="w-[48px] h-[45px] rounded-full"
                  />
                </div>
                <div
                  className="flex flex-col justify-center border-b-[1px] w-[90%] h-[65px] border-[rgb(239,232,232)] cursor-pointer"
                  onClick={() => {
                    setGroupId(group["group_id"]);
                  }}
                >
                  <div className="flex flex-col">
                    <div>{group["group_name"]}</div>
                    <div className="text-[0.7rem] text-[gray]">
                      {group["group_members"].join(", ")}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>
      {groupId === null ? (
        <section className="ml-[40%] bg-[#f0f2f5] h-screen flex flex-row justify-center items-center">
          <div>
            <img
              src={undrawChatting.src}
              alt="Undraw Chatting"
              className="h-[400px] w-[400px]"
            />
          </div>
        </section>
      ) : (
        <section className="ml-[40%]">
          <div className="flex flex-row justify-between fixed top-0 w-[100%] bg-[#f0f2f5] items-center pl-[15px] pt-[10px] pb-[10px] h-[4rem]">
            <div className="flex flex-row gap-2 items-center">
              <img
                src={dp.src}
                alt="profile picture"
                className="w-[40px] h-[40px] rounded-full"
              />
              {groupId && (
                <div>
                  <div>{getGroupName()}</div>
                  <div className="text-[0.75rem] text-[gray]">
                    {getGroupMembers().join(", ")}
                  </div>
                </div>
              )}
            </div>
          </div>
          <div className="chat-background h-screen bg-[#eae6df] mt-[4rem]">
            <div className="ml-[4rem] mt-[4rem] mr-[4rem] pt-[2rem]">
              {allChat.map((chat, idx) => {
                let justify =
                  chat["member"] == clientId ? "justify-end" : "justify-start";
                let bg_color =
                  chat["member"] == clientId ? "bg-[#d9fdd3]" : "bg-[white]";
                return (
                  <div
                    key={idx}
                    className={`flex flex-row w-[100%] ${justify}`}
                  >
                    <div
                      className={`rounded-[5px] ${bg_color} max-w-xs w-fit pl-[5px] py-[2px] pr-[25px] mb-[5px]`}
                    >
                      {chat["msg_body"]}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="flex flex-row justify-start gap-2 fixed bottom-0 w-[100%] bg-[#f0f2f5] items-center pl-[15px] pt-[10px] pb-[10px] h-[3.5rem]">
            <div className="w-[50%]">
              <OutlinedInput
                id="outlined-adornment-weight"
                size="small"
                value={message}
                fullWidth={false}
                sx={{
                  height: "2.35rem",
                  backgroundColor: "white",
                  width: "100%",
                }}
                onChange={(event) => {
                  setMessage(event.target.value);
                }}
                // onKeyDown={handleKeyDown}
                placeholder="Type a message"
              />
            </div>
            <div>
              <Button
                variant="contained"
                sx={{ color: "white" }}
                endIcon={<SendIcon sx={{ color: "white" }} />}
                onClick={handleSendMessage}
              >
                Send
              </Button>
            </div>
          </div>
        </section>
      )}

      {/* <div className="ml-[40%] bg-[#f0f2f5] h-screen">
        <div className="mb-10 flex flex-row gap-2">
          <TextField
            label="Group Name"
            variant="outlined"
            value={newGroupName}
            onChange={(event) => {
              setNewGroupName(event.target.value);
            }}
          />
          <TextField
            label="Group Members"
            variant="outlined"
            value={newGroupMembers}
            onChange={(event) => {
              setNewGroupMembers(event.target.value);
            }}
          />
          <TextField
            label="Group Admin"
            variant="outlined"
            value={newGroupAdmin}
            onChange={(event) => {
              setNewGroupAdmin(event.target.value);
            }}
          />
          <Button
            variant="contained"
            sx={{
              color: "white",
              boxShadow: "none",
            }}
            onClick={handleCreateGroup}
          >
            Create Group
          </Button>
        </div>
        <div className="mt-10 mb-10 flex flex-row gap-2">
          {groupList.map((group, idx) => {
            return (
              <Button
                key={idx}
                variant="contained"
                sx={{
                  color: "white",
                  boxShadow: "none",
                }}
                onClick={() => {
                  setGroupId(group["group_id"]);
                }}
              >
                {group["group_name"]}
              </Button>
            );
          })}
        </div>
        <TextField
          label="Send Message"
          variant="outlined"
          value={message}
          onChange={handleMessageChange}
        />
        <div className="abc">asda</div>
        <Button
          variant="contained"
          sx={{
            color: "white",
            boxShadow: "none",
          }}
          onClick={handleSendMessage}
        >
          Send
        </Button>
      </div>
      <div>
        {allChat.map((msg, idx) => {
          return (
            <div key={idx}>
              {msg["member"]}: {msg["msg_body"]}
            </div>
          );
        })}
      </div> */}
    </main>
  );
}
