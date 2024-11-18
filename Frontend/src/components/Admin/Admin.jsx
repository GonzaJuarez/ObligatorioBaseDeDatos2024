import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import { apiURL } from '../../const';


function Admin() {
  return (
    <div>
        <h1>Admin</h1>    
        <button onClick={ABMInstrucoresHandler}>ABM Instructores</button>
        <button onClick={ABMTurnosHandler}>ABM Turnos</button>
        <button onClick={ModActividadesHandler}>Modificar Actividades</button>
        <button onClick={ABMAlumnosHandler}>ABM Alumnos</button>
    </div>
  );
}

export default Admin;