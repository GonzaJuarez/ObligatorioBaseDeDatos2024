import React, { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Typography,
  Box,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Alert,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import "./Alumnos.css";
import Logout from "../Logout/Logout";

const Alumnos = () => {
  const [actividades, setActividades] = useState([]);
  const [equipamientos, setEquipamientos] = useState([]);
  const [turnos, setTurnos] = useState([]);
  const [actividadSeleccionada, setActividadSeleccionada] = useState("");
  const [equipamientoSeleccionado, setEquipamientoSeleccionado] =
    useState("ninguno");
  const [turnoSeleccionado, setTurnoSeleccionado] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStudentData = async () => {
      try {
        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) throw new Error("No se encontró el token de acceso");

        const response = await fetch("http://localhost:8000/datos_personales", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (!response.ok)
          throw new Error("Error al obtener los datos del alumno");

        const data = await response.json();
        console.log("Datos del alumno:", data);
        localStorage.setItem("ci", data.ci);
        console.log("CI alumno:", data.ci);
      } catch (error) {
        console.error("Error obteniendo la información del alumno:", error);
        setError(
          "No se pudo obtener la información del alumno. Intenta recargar la página."
        );
      }
    };

    fetchStudentData();
  }, []);

  // Cargar actividades desde el backend
  useEffect(() => {
    const fetchActividades = async () => {
      try {
        const response = await fetch("http://localhost:8000/actividades", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) throw new Error("Error al obtener las actividades");
        const data = await response.json();
        setActividades(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchActividades();
  }, []);

  // Cargar turnos desde el backend
  useEffect(() => {
    const fetchTurnos = async () => {
      try {
        const response = await fetch("http://localhost:8000/turnos", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) throw new Error("Error al obtener los turnos");
        const data = await response.json();
        setTurnos(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchTurnos();
  }, []);

  // Cargar equipamientos basados en la actividad seleccionada
  useEffect(() => {
    if (actividadSeleccionada) {
      const fetchEquipamientos = async () => {
        try {
          const response = await fetch(
            `http://localhost:8000/equipamiento/actividad/${actividadSeleccionada}`,
            {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          if (!response.ok)
            throw new Error("Error al obtener los equipamientos");
          const data = await response.json();
          setEquipamientos(data);
        } catch (error) {
          console.error("Error:", error);
        }
      };
      fetchEquipamientos();
    }
  }, [actividadSeleccionada]);

  // Manejar el envío del formulario de inscripción
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    try {
      // Verificar disponibilidad del profesor (si hay un endpoint para esto)
      const response = await fetch(
        `http://localhost:8000/clases/disponibilidad/${turnoSeleccionado}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok)
        throw new Error(
          "No hay profesor disponible para esta actividad y turno"
        );
      const data = await response.json();
      console.log(data);
      if (!data.instructor_disponible)
        throw new Error(
          "No hay profesor disponible para esta actividad y turno"
        );

      const instructor = data.instructor_ci;

      // Realizar la inscripción parte 1: post a clases
      const inscripcionResponse = await fetch("http://localhost:8000/clases", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ci_instructor: instructor,
          id_actividad: actividadSeleccionada,
          id_turno: turnoSeleccionado,
          dictada: false,
        }),
      });

      if (!inscripcionResponse.ok)
        throw new Error("Error al realizar la inscripción: post a clases");

      const dataClase = await inscripcionResponse.json();
      const idClase = dataClase.id;
      //Realizar la inscripción parte 2: post a clase_alumno
      const inscripcionResponse2 = await fetch(
        "http://localhost:8000/alumno_clase",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            id_clase: idClase,
            ci_alumno: localStorage.getItem("ci"),
            id_equipamiento: equipamientoSeleccionado,
          }),
        }
      );
      if (!inscripcionResponse2.ok)
        throw new Error(
          "Error al realizar la inscripción: post a clase_alumno"
        );
      setSuccess(true);
    } catch (error) {
      console.error("Error:", error);
      setError(
        "No se pudo completar la inscripción. Por favor, intenta nuevamente."
      );
    }
  };

  return (
    <Box className="inscripcion-box">
      <Logout />
      <Typography variant="h4" component="h1" className="inscripcion-title">
        Inscripción a Clases
      </Typography>
      <form onSubmit={handleSubmit}>
        <FormControl fullWidth className="form-field" required>
          <InputLabel id="actividad-label">Actividad</InputLabel>
          <Select
            labelId="actividad-label"
            value={actividadSeleccionada}
            onChange={(e) => setActividadSeleccionada(e.target.value)}
          >
            {actividades.map((actividad) => (
              <MenuItem key={actividad.id} value={actividad.id}>
                {actividad.nombre}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth className="form-field">
          <InputLabel id="equipamiento-label">
            Equipamiento (Opcional)
          </InputLabel>
          <Select
            labelId="equipamiento-label"
            value={equipamientoSeleccionado}
            onChange={(e) => setEquipamientoSeleccionado(e.target.value)}
          >
            <MenuItem value="ninguno">Ninguno</MenuItem>
            {equipamientos.map((equipamiento) => (
              <MenuItem key={equipamiento.id} value={equipamiento.id}>
                {equipamiento.nombre}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth className="form-field" required>
          <InputLabel id="turno-label">Turno</InputLabel>
          <Select
            labelId="turno-label"
            value={turnoSeleccionado}
            onChange={(e) => setTurnoSeleccionado(e.target.value)}
          >
            {turnos.map((turno) => (
              <MenuItem key={turno.id} value={turno.id}>
                {turno.horario}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        {error && (
          <Box className="form-field">
            <Alert severity="error">{error}</Alert>
          </Box>
        )}
        {success && (
          <Box className="form-field">
            <Alert severity="success">Inscripción exitosa</Alert>
          </Box>
        )}
        <Button type="submit" variant="contained" fullWidth>
          Inscribirse
        </Button>
        <Button
          variant="text"
          fullWidth
          className="ver-clases-button"
          onClick={() => navigate("/alumnos/mis-clases")}
        >
          Ver Mis Clases
        </Button>
      </form>
    </Box>
  );
};

export default Alumnos;
