import React, { useEffect, useState } from "react";
import styled from "styled-components";
import NavBar from "./NavBar";
import Login from "../pages/Login";
import NotesPage from "../pages/Notes";
import { apiFetch } from "../api";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    apiFetch("/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }).then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      } else {
        localStorage.removeItem("token");
      }
    });
  }, []);

  const onLogin = (token, user) => {
    localStorage.setItem("token", token);
    setUser(user);
  };

  const content = user ? <NotesPage user={user} /> : <Login onLogin={onLogin} />;

  return (
    <PageShell>
      <BackgroundArt aria-hidden="true" />
      <FloatingButton aria-label="Quick actions">◌</FloatingButton>
      {user ? <NavBar setUser={setUser} /> : null}
      <AppContent>{content}</AppContent>
    </PageShell>
  );
}

const PageShell = styled.div`
  position: relative;
  min-height: 100vh;
  overflow: hidden;
`;

const BackgroundArt = styled.div`
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 10% 91%, rgba(255, 89, 179, 0.8), transparent 25%),
    radial-gradient(circle at 48% 18%, rgba(255, 255, 255, 0.22), transparent 22%),
    linear-gradient(120deg, rgba(255, 31, 157, 0.78), rgba(139, 51, 212, 0.75) 32%, rgba(28, 80, 171, 0.9) 100%);
  opacity: 1;

  &::before,
  &::after {
    content: "";
    position: absolute;
    inset: -12% -10% -10% -10%;
    pointer-events: none;
    background-repeat: no-repeat;
    background-size: cover;
  }

  &::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'%3E%3Cg fill='none' stroke='rgba(255,255,255,0.52)' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M-40 420 C 220 300, 290 620, 580 470 S 1020 250, 1640 420' /%3E%3Cpath d='M-30 500 C 240 350, 260 760, 620 560 S 1040 380, 1650 550' /%3E%3Cpath d='M0 620 C 220 520, 360 800, 640 690 S 1080 520, 1600 660' /%3E%3Cpath d='M-20 310 C 180 260, 360 360, 640 300 S 1120 180, 1640 330' /%3E%3Cpath d='M0 700 C 250 550, 420 920, 740 760 S 1160 610, 1600 760' /%3E%3C/g%3E%3C/svg%3E");
    opacity: 0.75;
    transform: scale(1.15);
    filter: blur(2px);
  }

  &::after {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'%3E%3Cg fill='none' stroke='rgba(255,255,255,0.28)' stroke-width='3' stroke-linecap='round'%3E%3Cpath d='M-30 470 C 180 320, 360 650, 640 480 S 1120 250, 1650 500' /%3E%3Cpath d='M-20 620 C 220 440, 330 780, 700 620 S 1190 430, 1600 620' /%3E%3C/g%3E%3C/svg%3E");
    opacity: 0.9;
    transform: scale(1.05);
  }
`;

const AppContent = styled.div`
  position: relative;
  z-index: 1;
`;

const FloatingButton = styled.button`
  position: fixed;
  left: 24px;
  bottom: 18px;
  z-index: 2;
  width: 60px;
  height: 60px;
  border: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(8px);
  box-shadow: 0 18px 30px rgba(52, 24, 92, 0.25);
  color: #fff;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  @media (max-width: 640px) {
    width: 50px;
    height: 50px;
    left: 14px;
    bottom: 12px;
    font-size: 1.5rem;
  }
`;

export default App;
