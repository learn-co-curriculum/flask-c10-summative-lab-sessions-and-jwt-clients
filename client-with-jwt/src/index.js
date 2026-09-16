import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";
import { BrowserRouter } from "react-router-dom";
import { createGlobalStyle } from "styled-components";

const GlobalStyle = createGlobalStyle`
  *,
  *::before, 
  *::after {
    box-sizing: border-box;
  }

  html, body {
    margin: 0;
  }

  body {
    min-height: 100vh;
    margin: 0;
    background: linear-gradient(135deg, #ff1aa9 0%, #bd3ae5 26%, #4c3ad4 56%, #0d3e8d 100%);
    font-family: BlinkMacSystemFont,-apple-system,"Segoe UI",Roboto,Oxygen,Ubuntu,Cantarell,"Fira Sans","Droid Sans","Helvetica Neue",Helvetica,Arial,sans-serif;
    color: #4c1735;
  }

  #root {
    min-height: 100vh;
  }
`;

ReactDOM.render(
  <BrowserRouter>
    <GlobalStyle />
    <App />
  </BrowserRouter>,
  document.getElementById("root")
);
