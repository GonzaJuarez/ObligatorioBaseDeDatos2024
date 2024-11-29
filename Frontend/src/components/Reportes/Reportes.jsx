import React, { useState, useEffect } from "react";
import { Button, Typography, Box, CircularProgress } from "@mui/material";
import { apiURL } from "../../const";
import "./Reportes.css";
import Logout from "../Logout/Logout";

function Reportes() {
  const [dataGanancias, setDataGanancias] = useState(null);
  const [dataAlumnos, setDataAlumnos] = useState(null);
  const [dataTurnos, setDataTurnos] = useState(null);

  const fetchActividadesMasGanancias = async () => {
    try {
      const response = await fetch(`${apiURL}actividades_mas_ganancias`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Error al obtener reportes");
      }
      const data = await response.json();
      setDataGanancias(data);
      console.log("Reportes:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const fetchActividadesMasAlumnos = async () => {
    try {
      const response = await fetch(`${apiURL}actividades_mas_alumnos`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Error al obtener reportes");
      }
      const data = await response.json();
      setDataAlumnos(data);
      console.log("Reportes:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const fetchTurnosMasDictados = async () => {
    try {
      const response = await fetch(`${apiURL}turnos_mas_dictados`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Error al obtener reportes");
      }
      const data = await response.json();
      setDataTurnos(data);
      console.log("Reportes:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    fetchActividadesMasGanancias();
    fetchTurnosMasDictados();
    fetchActividadesMasAlumnos();
  }, []);

  return (
    <div>
      <Logout />
      <div className="reportes-container">
        <Button
          variant="outlined"
          onClick={() => (window.location.href = "/Admin")}
          className="back-button"
        >
          Volver
        </Button>

        <Typography variant="h4" component="h1" className="reportes-title">
          Reportes
        </Typography>

        <Typography variant="h6" className="reportes-subtitle">
          Actividad con más ganancias:
        </Typography>
        {dataGanancias ? (
          <div>
            <p>
              <strong>Actividad:</strong> {dataGanancias.actividad}
            </p>
            <p>
              <strong>Ganancias:</strong>{" "}
              {dataGanancias.ingresos !== null
                ? dataGanancias.ingresos
                : "No disponibles"}
            </p>
          </div>
        ) : (
          <p>Cargando...</p>
        )}

        <Typography variant="h6" className="reportes-subtitle">
          Actividad con más alumnos:
        </Typography>
        {dataAlumnos ? (
          <div>
            <p>
              <strong>Actividad:</strong> {dataAlumnos.actividad}
            </p>
            <p>
              <strong>Cantidad de alumnos:</strong>{" "}
              {dataAlumnos.cantidad_alumnos !== null
                ? dataAlumnos.cantidad_alumnos
                : "No disponibles"}
            </p>
          </div>
        ) : (
          <p>Cargando...</p>
        )}

        <Typography variant="h6" className="reportes-subtitle">
          Turno más dictado:
        </Typography>
        {dataTurnos ? (
          <div>
            <p>
              <strong>Inicio de turno:</strong>{" "}
              {new Date(dataTurnos.inicio_turno * 1000).toLocaleTimeString()}
            </p>
            <p>
              <strong>Fin de turno:</strong>{" "}
              {new Date(dataTurnos.fin_turno * 1000).toLocaleTimeString()}
            </p>
            <p>
              <strong>Total de clases:</strong>{" "}
              {dataTurnos.total_clases !== null
                ? dataTurnos.total_clases
                : "No disponibles"}
            </p>
          </div>
        ) : (
          <p>Cargando...</p>
        )}
      </div>
    </div>
  );
}

export default Reportes;
