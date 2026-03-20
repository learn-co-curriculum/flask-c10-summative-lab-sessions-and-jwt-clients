import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import Login from "../pages/Login";

function App() {
  const [user, setUser] = useState(null);
  // Tracks whether the /check_session fetch has finished so we don't
  // flash the Login page on every refresh before the response arrives.
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/check_session", {
      // credentials: "include" ensures the session cookie is sent
      // with the request (required when the API is on a different port)
      credentials: "include",
    })
      .then((r) => {
        if (r.ok) {
          return r.json().then((user) => setUser(user));
        }
        // No active session — user will be shown the Login page
      })
      .finally(() => setLoading(false));
  }, []);

  // Called by NavBar's logout button — clears user state after the
  // server has ended the session via DELETE /logout
  const onLogout = () => {
    fetch("/logout", {
      method: "DELETE",
      credentials: "include",
    }).then((r) => {
      if (r.ok) setUser(null);
    });
  };

  // Avoid a Login flash while the /check_session fetch is in-flight
  if (loading) return null;

  if (!user) return <Login onLogin={setUser} />;

  return (
    <>
      <NavBar user={user} setUser={setUser} onLogout={onLogout} />
      <main>
        <p>You are logged in!</p>
      </main>
    </>
  );
}

export default App;