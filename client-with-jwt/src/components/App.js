import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import Login from "../pages/Login";

function App() {
  const [user, setUser] = useState(null);
  // Tracks whether the /me check has finished so we don't flash the
  // Login page on every refresh before the fetch completes.
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    // No token stored — skip the fetch and go straight to Login
    if (!token) {
      setLoading(false);
      return;
    }

    fetch("/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((r) => {
        if (r.ok) {
          return r.json().then((user) => setUser(user));
        }
        // Token is expired or invalid — clear it so the user sees Login
        localStorage.removeItem("token");
      })
      .finally(() => setLoading(false));
  }, []);

  const onLogin = (token, user) => {
    localStorage.setItem("token", token);
    setUser(user);
  };

  // Called by NavBar's logout button
  const onLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  // Avoid a Login flash while the /me fetch is in-flight
  if (loading) return null;

  if (!user) return <Login onLogin={onLogin} />;

  return (
    <>
      <NavBar setUser={setUser} onLogout={onLogout} />
      <main>
        <p>You are logged in!</p>
      </main>
    </>
  );
}

export default App;