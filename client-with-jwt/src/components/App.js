import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import Login from "../pages/Login";
import NotesList from "./NotesList";   // ← add this

function App() {
  const [user, setUser] = useState(null);
  const token = localStorage.getItem("token");  // ← read token once

  useEffect(() => {
    fetch("/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }).then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  const onLogin = (token, user) => {
    localStorage.setItem("token", token);
    setUser(user);
  };

  if (!user) return <Login onLogin={onLogin} />;

  return (
    <>
      <NavBar setUser={setUser} />
      <main>
        <h2>Welcome, {user.username}!</h2>
        <NotesList token={token} />   {/* ← render notes here */}
      </main>
    </>
  );
}

export default App;