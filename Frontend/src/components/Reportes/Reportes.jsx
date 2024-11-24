import React, { useState, useEffect } from "react";
import { apiURL } from "../../const";

function Reportes() {
    const [dataGanancias, setDataGanancias] = useState(null);
    const [dataAlumnos, setDataAlumnos] = useState(null);
    const [dataTurnos, setDataTurnos] = useState(null);

    // Definir la función para obtener los datos
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


    // Usar useEffect para llamar la función al montar el componente
    useEffect(() => {
        fetchActividadesMasGanancias();
        fetchTurnosMasDictados();
        fetchActividadesMasAlumnos();
    }, []);

    return (
        <div>
            <button onClick={() => window.location.href = "/Admin"}>Volver</button>
            <h1>Reportes</h1>
            <h2>Actividad con más ganancias:</h2>
            {dataGanancias ? (
                <pre>{JSON.stringify(dataGanancias, null, 2)}</pre>
            ) : (
                <p>Cargando...</p>
            )}
            <h2>Actividad con más alumnos:</h2>
            {dataAlumnos ? (
                <pre>{JSON.stringify(dataAlumnos, null, 2)}</pre>
            ) : (
                <p>Cargando...</p>
            )}
            <h2>Turno más dictado:</h2>
            {dataTurnos ? (
                <pre>{JSON.stringify(dataTurnos, null, 2)}</pre>
            ) : (
                <p>Cargando...</p>
            )}
        </div>
    );
}

export default Reportes;
