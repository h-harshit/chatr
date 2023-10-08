import { combineReducers } from "redux";
import { allChatReducers } from "./chatReducers";

const rootReducer = combineReducers({
  allChat: allChatReducers,
});

export default rootReducer;
