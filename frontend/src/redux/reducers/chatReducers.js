let allChat = [];
export const allChatReducers = (state = allChat, action) => {
  switch (action.type) {
    case "SET_ALL_CHAT":
      state = action.payload;
      return state;
    default:
      return state;
  }
};
