import React, { useState } from "react";
import LoginForm from "../components/LoginForm";
import SignUpForm from "../components/SignUpForm";
import styled from "styled-components";

function Login({ onLogin }) {
  const [isSignUp, setIsSignUp] = useState(false);

  return (
    <Container>
      <NavBar>
        <Logo>MyApp</Logo>
      </NavBar>
      <Card>
        <Header>
          <h2>{isSignUp ? "Sign Up" : "Login"}</h2>
          <ToggleButton>
            {isSignUp ? (
              <>
                Already have an account?{" "}
                <Link onClick={() => setIsSignUp(false)}>Login here</Link>
              </>
            ) : (
              <>
                Don't have an account?{" "}
                <Link onClick={() => setIsSignUp(true)}>Sign up here</Link>
              </>
            )}
          </ToggleButton>
        </Header>
        {isSignUp ? (
          <SignUpForm onLogin={onLogin} />
        ) : (
          <LoginForm onLogin={onLogin} />
        )}
      </Card>
    </Container>
  );
}

const Container = styled.div`
  min-height: 100vh;
  background: white;
  padding: 16px;
  display: flex;
  flex-direction: column;
`;

const NavBar = styled.header`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
`;

const Logo = styled.h1`
  font-family: "Permanent Marker", cursive;
  font-size: 3rem;
  color: deeppink;
  margin: 0;
  line-height: 1;
`;

const Card = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 40px;
  max-width: 400px;
  width: 100%;
  margin: 20px auto;
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: 30px;

  h2 {
    margin: 0 0 16px 0;
    color: #333;
    font-size: 28px;
  }
`;

const ToggleButton = styled.p`
  margin: 0;
  color: #666;
  font-size: 14px;
`;

const Link = styled.span`
  color: #667eea;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;

  &:hover {
    color: #764ba2;
    text-decoration: underline;
  }
`;

export default Login;