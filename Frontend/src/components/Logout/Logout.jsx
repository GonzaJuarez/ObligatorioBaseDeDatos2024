import React from "react";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "./Logout.css";

const Logout = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_role");
    navigate("/login");
  };

  return (
    <Button
      variant="contained"
      className="logout-button"
      onClick={handleLogout}
    >
      Cerrar Sesión
    </Button>
  );
};

export default Logout;
