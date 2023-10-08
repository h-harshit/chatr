"use client";
import * as React from "react";
import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import TextField from "@mui/material/TextField";

export default function TextInput(props) {
  return (
    <Box sx={{ "& > :not(style)": { m: 1 } }}>
      <FormControl variant="standard">
        <Box sx={{ display: "flex", alignItems: "flex-end" }}>
          {props.inputAdornment}
          <TextField
            label={props.label}
            variant="standard"
            value={props.value}
            onChange={props.onChange}
          />
        </Box>
      </FormControl>
    </Box>
  );
}
