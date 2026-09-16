import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

function NavBar({ setUser }) {
  function handleLogoutClick() {
    localStorage.removeItem("token");
    setUser(null);
  }

  return (
    <Wrapper>
      <Logo>
        <Link to="/">My App</Link>
      </Logo>
      <Nav>
        <LogoutButton type="button" onClick={handleLogoutClick}>
          Logout
        </LogoutButton>
      </Nav>
    </Wrapper>
  );
}

const Wrapper = styled.header`
  position: sticky;
  top: 12px;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 14px auto 0;
  padding: 14px 22px;
  background: rgba(255, 255, 255, 0.24);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.38);
  border-radius: 18px;
  box-shadow: 0 12px 24px rgba(72, 33, 109, 0.15);
`;

const Logo = styled.h1`
  font-family: "Permanent Marker", cursive;
  font-size: 2.7rem;
  color: #4a1a5c;
  margin: 0;
  line-height: 1;

  a {
    color: inherit;
    text-decoration: none;
  }
`;

const Nav = styled.nav`
  display: flex;
  align-items: center;
`;

const LogoutButton = styled.button`
  border: 1px solid rgba(74, 26, 92, 0.3);
  background: linear-gradient(135deg, #d8c6ff 0%, #b99ef7 100%);
  color: #2c0d3e;
  border-radius: 10px;
  padding: 10px 18px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(96, 78, 159, 0.18);
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 24px rgba(96, 78, 159, 0.22);
  }
`;

export default NavBar;
