import React, { useState } from "react";
import styled from "styled-components";
import { Button, Error, Input, FormField, Label } from "../styles";
import { apiFetch } from "../api";

function SignUpForm({ onSignupSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [errors, setErrors] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setErrors([]);
    setIsLoading(true);

    apiFetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
        password_confirmation: passwordConfirmation,
      }),
    })
      .then(async (r) => {
        const payload = r.headers.get("Content-Type")?.includes("application/json")
          ? await r.json()
          : {};

        if (r.ok) {
          setUsername("");
          setPassword("");
          setPasswordConfirmation("");
          if (onSignupSuccess) onSignupSuccess();
          return;
        }

        setErrors(payload.errors || ["Sign up failed."]);
      })
      .catch(() => {
        setErrors(["Unable to reach the server. Please make sure the app is running."]);
      })
      .finally(() => setIsLoading(false));
  }

  return (
    <form onSubmit={handleSubmit}>
      <FormField>
        <Label htmlFor="username">Username</Label>
        <Input
          type="text"
          id="username"
          autoComplete="off"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </FormField>
      <FormField>
        <Label htmlFor="password">Password</Label>
        <PasswordRow>
          <Input
            type={showPassword ? "text" : "password"}
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="new-password"
          />
          <ToggleButton
            type="button"
            onClick={() => setShowPassword((current) => !current)}
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? "Hide" : "Show"}
          </ToggleButton>
        </PasswordRow>
      </FormField>
      <FormField>
        <Label htmlFor="password_confirmation">Password Confirmation</Label>
        <PasswordRow>
          <Input
            type={showConfirmation ? "text" : "password"}
            id="password_confirmation"
            value={passwordConfirmation}
            onChange={(e) => setPasswordConfirmation(e.target.value)}
            autoComplete="new-password"
          />
          <ToggleButton
            type="button"
            onClick={() => setShowConfirmation((current) => !current)}
            aria-label={showConfirmation ? "Hide confirmation password" : "Show confirmation password"}
          >
            {showConfirmation ? "Hide" : "Show"}
          </ToggleButton>
        </PasswordRow>
      </FormField>
      <FormField>
        <Button type="submit">{isLoading ? "Loading..." : "Sign Up"}</Button>
      </FormField>
      <FormField>
        {errors.map((err) => (
          <Error key={err}>{err}</Error>
        ))}
      </FormField>
    </form>
  );
}

const PasswordRow = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const ToggleButton = styled.button`
  border: 1px solid rgba(122, 92, 231, 0.35);
  background: rgba(255, 255, 255, 0.7);
  color: #4b3d60;
  border-radius: 8px;
  padding: 9px 10px;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;

  &:hover {
    background: rgba(122, 92, 231, 0.08);
    transform: translateY(-1px);
  }
`;

export default SignUpForm;
