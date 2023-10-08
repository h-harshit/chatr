"use client";
import "./globals.css";
import { ThemeProvider } from "@mui/material/styles";
import { chatrTheme } from "@/themes/chatrMuiTheme";
import { Provider } from "react-redux";
import { store } from "../redux/store";

const metadata = {
  title: "Chatter",
  description: "Group Chat Application",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Provider store={store}>
          <ThemeProvider theme={chatrTheme}>{children}</ThemeProvider>
        </Provider>
      </body>
    </html>
  );
}
