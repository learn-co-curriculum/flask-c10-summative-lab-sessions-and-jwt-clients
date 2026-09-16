import styled from "styled-components";

const COLORS = {
  primary: {
    "--main": "#c9b7ff",
    "--accent": "#2b0d3d",
  },
  secondary: {
    "--main": "#f0d8ff",
    "--accent": "#4d2a82",
  },
};

function Button({ variant = "fill", color = "primary", ...props }) {
  let Component;
  if (variant === "fill") {
    Component = FillButton;
  } else if (variant === "outline") {
    Component = OutlineButton;
  }

  return <Component style={COLORS[color]} {...props} />;
}

const ButtonBase = styled.button`
  cursor: pointer;
  font-size: 1rem;
  border: 1px solid transparent;
  border-radius: 6px;
  padding: 8px 16px;
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease, background 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 18px rgba(91, 72, 156, 0.18);
  }

  &:active {
    transform: translateY(0);
  }
`;

const FillButton = styled(ButtonBase)`
  background: #c9b7ff;
  color: var(--accent);
  box-shadow: 0 10px 24px rgba(171, 144, 255, 0.2);

  &:hover {
    filter: brightness(1.06);
  }
`;

const OutlineButton = styled(ButtonBase)`
  background: rgba(255, 255, 255, 0.2);
  color: var(--main);
  border: 2px solid rgba(198, 178, 255, 0.9);

  &:hover {
    background: rgba(255, 255, 255, 0.34);
  }
`;

export default Button;
