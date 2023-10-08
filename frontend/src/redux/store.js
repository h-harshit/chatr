"use client";
import { createStore, applyMiddleware, compose } from "redux";
import { createWrapper } from "next-redux-wrapper";
import rootReducer from "./reducers/";

export const makeStore = () => {
  let store;
  // const middleware = [thunk];

  store = createStore(rootReducer);
  return store;
};
export const store = makeStore();
// const makeStore = () =>
//   createStore(rootReducer, compose(applyMiddleware(...middleware)));

export const wrapper = createWrapper(makeStore);
