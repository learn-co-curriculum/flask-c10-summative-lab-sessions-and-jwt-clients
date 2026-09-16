import { useState } from "react";
import styled from "styled-components";
import LoginForm from "../components/LoginForm";
import SignUpForm from "../components/SignUpForm";
import { Button } from "../styles";

function Login({ onLogin }) {
  const [showLogin, setShowLogin] = useState(true);

  return (
    <PageWrap>
      <IntroCard>
        <BadgeRow>
          <Badge>Notes</Badge>
          <Badge>Tasks</Badge>
          <Badge>Workouts</Badge>
          <Badge>Journal</Badge>
        </BadgeRow>
        <Logo>My App</Logo>
        <HeaderTitle>Organize your life in one place</HeaderTitle>
        <HeaderText>
          Keep track of your notes, tasks, workouts, and journal entries in a secure,
          personal dashboard built for everyday planning and reflection.
        </HeaderText>
      </IntroCard>

      <Wrapper>
        {showLogin ? (
          <>
            <LoginForm onLogin={onLogin} />
            <Divider />
            <p>
              Don't have an account? &nbsp;
              <Button color="secondary" onClick={() => setShowLogin(false)}>
                Sign Up
              </Button>
            </p>
          </>
        ) : (
          <>
            <SignUpForm onSignupSuccess={() => setShowLogin(true)} />
            <Divider />
            <p>
              Already have an account? &nbsp;
              <Button color="secondary" onClick={() => setShowLogin(true)}>
                Log In
              </Button>
            </p>
          </>
        )}
      </Wrapper>
    </PageWrap>
  );
}

const PageWrap = styled.div`
  width: min(100%, 980px);
  margin: 32px auto 40px;
  padding: 0 20px;

  @media (max-width: 640px) {
    margin: 20px auto 28px;
    padding: 0 14px;
  }
`;

const IntroCard = styled.section`
  margin: 0 auto 22px;
  width: min(100%, 920px);
  padding: 28px 30px 24px;
  background: linear-gradient(135deg, rgba(255,255,255,0.26), rgba(255,255,255,0.12));
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 30px;
  box-shadow: 0 20px 44px rgba(87, 48, 124, 0.18);
  position: relative;
  overflow: hidden;

  @media (max-width: 640px) {
    padding: 20px 18px 18px;
    border-radius: 22px;
  }

  &::before,
  &::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
  }

  &::before {
    width: 220px;
    height: 220px;
    right: -40px;
    top: -70px;
    background: radial-gradient(circle, rgba(255,255,255,0.42), rgba(255,255,255,0));
  }

  &::after {
    width: 260px;
    height: 260px;
    left: -20px;
    bottom: -110px;
    background: radial-gradient(circle, rgba(255, 146, 219, 0.32), rgba(255,255,255,0));
  }
`;

const BadgeRow = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
  position: relative;
  z-index: 1;
`;

const Badge = styled.span`
  border: 1px solid rgba(92, 48, 134, 0.14);
  background: rgba(255, 255, 255, 0.4);
  color: #46225c;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  box-shadow: 0 8px 18px rgba(113, 69, 143, 0.08);
`;

const Logo = styled.h1`
  font-family: "Permanent Marker", cursive;
  font-size: clamp(2.6rem, 4vw, 4rem);
  color: #4d1a5d;
  margin: 0 0 10px;
  position: relative;
  z-index: 1;
  text-shadow: 0 12px 24px rgba(256, 255, 255, 0.2);
`;

const HeaderTitle = styled.h2`
  margin: 0 0 10px;
  color: #2f1d3c;
  font-size: clamp(1.8rem, 3vw, 3rem);
  line-height: 1.1;
  position: relative;
  z-index: 1;
`;

const HeaderText = styled.p`
  margin: 0;
  color: rgba(52, 31, 62, 0.9);
  line-height: 1.6;
  font-size: 1.05rem;
  max-width: 680px;
  position: relative;
  z-index: 1;

  @media (max-width: 640px) {
    font-size: 0.95rem;
    line-height: 1.5;
  }
`;

const Wrapper = styled.section`
  width: min(100%, 440px);
  margin: 0 auto;
  padding: 28px 24px 20px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.45);
  border-radius: 22px;
  box-shadow: 0 18px 36px rgba(120, 66, 128, 0.18);

  @media (max-width: 640px) {
    width: 100%;
    padding: 20px 16px 16px;
    border-radius: 18px;
  }
`;

const Divider = styled.hr`
  border: none;
  border-bottom: 1px solid rgba(255, 79, 163, 0.2);
  margin: 16px 0;
`;

export default Login;
