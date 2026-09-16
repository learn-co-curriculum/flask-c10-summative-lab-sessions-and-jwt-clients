import styled from "styled-components";

const Input = styled.input`
  border-radius: 10px;
  border: 1px solid rgba(122, 92, 231, 0.3);
  background: rgba(255, 255, 255, 0.9);
  -webkit-appearance: none;
  max-width: 100%;
  width: 100%;
  font-size: 1rem;
  line-height: 1.5;
  padding: 10px 12px;
  box-shadow: inset 0 1px 3px rgba(160, 70, 120, 0.08);
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;

  &:hover {
    border-color: rgba(122, 92, 231, 0.6);
    box-shadow: 0 0 0 3px rgba(122, 92, 231, 0.08);
  }

  &:focus {
    outline: none;
    border-color: rgba(122, 92, 231, 0.9);
    box-shadow: 0 0 0 4px rgba(122, 92, 231, 0.12);
    transform: translateY(-1px);
  }
`;

export default Input;
