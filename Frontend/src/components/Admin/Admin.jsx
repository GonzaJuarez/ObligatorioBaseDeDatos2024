import React from "react";
import { Box, Typography, Button } from "@mui/material";
import Manager from "../Manager/Manager";
import Logout from "../Logout/Logout";
import "./admin.css";

const Admin = () => {
  return (
    <div className="admin-background">
      <Logout />
      <Box className="admin-container">
        <Typography variant="h4" component="h1" className="admin-title">
          Admin Panel
        </Typography>
        <Box className="managers-container">
          <Manager category="Instructores" />
          <Manager category="Turnos" />
          <Manager category="Actividades" />
          <Manager category="Alumnos" />
          <Manager category="Equipamiento" />
        </Box>
        <Button
          variant="contained"
          className="admin-button"
          onClick={() => (window.location.href = "/Admin/Reportes")}
        >
          Ver Reportes
        </Button>
      </Box>
    </div>
  );
};

export default Admin;
