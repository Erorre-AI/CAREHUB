import React, { useState } from "react";
import { Box, CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import ChatWindow from "./components/ChatWindow";
import ToggleTheme from "./components/ToggleTheme";

const App = () => {
  const [darkMode, setDarkMode] = useState(false);

  const theme = createTheme({
    palette: {
      mode: darkMode ? "dark" : "light",
      primary: {
        main: darkMode ? "#075e54" : "#25d366", // WhatsApp green
      },
      background: {
        default: darkMode ? "#121212" : "#f5f5f5",
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          height: "100vh",
          padding: "16px",
        }}
      >
        <ToggleTheme darkMode={darkMode} setDarkMode={setDarkMode} />
        <ChatWindow />
      </Box>
    </ThemeProvider>
  );
};

export default App;