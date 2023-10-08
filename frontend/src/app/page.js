"use client";

import Image from "next/image";
import undrawHomeImg from "../assets/svg/undraw_group_chat.svg";
import logoTransparent from "../assets/logo/chatr_transparent_bg_logo.png";
import SmartphoneIcon from "@mui/icons-material/Smartphone";
import TextInput from "@/components/inputs/TextInput";
import { useEffect, useState } from "react";
import Button from "@mui/material/Button";
import { useRouter } from "next/navigation";

export default function Home() {
  const [mobileNumber, setMobileNumber] = useState("");
  const router = useRouter();

  const clientId = localStorage.getItem("client_id");

  useEffect(() => {
    if (clientId) {
      router.push("/chat");
    }
  }, []);

  const handleMobileNumberChange = (event) => {
    setMobileNumber(event.target.value);
  };

  const handleLogin = (event) => {
    localStorage.setItem("client_id", mobileNumber);
    router.push("/chat");
  };

  return (
    <main id="home-main-container">
      <div className="flex flex-row mt-20 ml-40 mr-40 rounded-[2rem]  shadow-2xl">
        <div className="w-[40%] h-[70vh] rounded-[2rem] flex flex-col gap-[5rem]">
          <div className="mt-8 flex flex-row justify-center">
            <Image src={logoTransparent} height={100} width={170} />
          </div>
          <div className="flex flex-col gap-3">
            <div className="flex flex-row justify-center">
              <TextInput
                label="Mobile Number"
                value={mobileNumber}
                onChange={handleMobileNumberChange}
                inputAdornment={
                  <SmartphoneIcon sx={{ color: "#38b2ab", mr: 1, my: 0.5 }} />
                }
              />
            </div>
            <div className="flex flex-row justify-center">
              <Button
                variant="contained"
                className="flex flex-row"
                sx={{
                  color: "white",
                  boxShadow: "none",
                  borderRadius: "2rem",
                  fontSize: "0.8rem",
                }}
                onClick={handleLogin}
              >
                OTP Login
              </Button>
            </div>
          </div>
        </div>
        <div className="w-[60%] bg-primary-light h-[70vh] rounded-r-[2rem] flex flex-row justify-center items-center">
          <Image src={undrawHomeImg} height={400} width={400} />
        </div>
      </div>
    </main>
  );
}
