import React, { useState } from "react";
import { TextField, Button, Typography, Alert, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "./Login.css"; // Importa el archivo CSS

const Login = () => {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/login/confirm", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ correo, contrasena: password }),
      });

      if (!response.ok) {
        throw new Error("Login fallido");
      }

      const data = await response.json();
      localStorage.setItem("access_token", data.access_token);
      const datosPersonalesResponse = await fetch(
        "http://localhost:8000/datos_personales",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${data.access_token}`,
          },
        }
      );

      if (!datosPersonalesResponse.ok) {
        throw new Error("Error al obtener datos personales");
      }

      const datos = await datosPersonalesResponse.json();
      const id_rol = datos.rol;
      console.log("datos:", datos);
      localStorage.setItem("user_role", id_rol); // Almacenar el rol del usuario
      console.log("ID ROL:", id_rol);

      setError("");
      if ([1, 2].includes(id_rol)) {
        navigate("/admin");
      } else {
        navigate("/alumnos");
      }
    } catch (error) {
      console.error("Error:", error);
      setError("Login fallido. Verifica tus credenciales.");
    }
  };

  const handleRegisterRedirect = () => {
    navigate("/signup");
  };

  return (
    <div>
      <Box className="login-box">
        <Typography variant="h4" component="h1" className="login-title">
          Winter Games Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <Box className="form-field">
            <TextField
              label="Correo"
              variant="outlined"
              fullWidth
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              required
            />
          </Box>
          <Box className="form-field">
            <TextField
              label="contraseña"
              variant="outlined"
              type="password"
              fullWidth
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </Box>
          {error && (
            <Box className="form-field">
              <Alert severity="error">{error}</Alert>
            </Box>
          )}
          <Button
            type="submit"
            variant="contained"
            fullWidth
            className="login-button"
          >
            Ingresar
          </Button>
          <Button
            variant="text"
            fullWidth
            className="register-button"
            onClick={handleRegisterRedirect}
            sx={{
              backgroundColor: "transparent",
              "&:hover": {
                backgroundColor: "transparent",
                color: "#115293",
              },
            }}
          >
            ¿No tenés cuenta? Registrate
          </Button>
        </form>
      </Box>
    </div>
  );
};

export default Login;
