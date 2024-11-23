import React from 'react';
import Manager from '../Manager/Manager';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { apiURL } from '../../const';


function Admin() {
  return (
    <div>
        <h1>Admin</h1>    
        <Manager category="Instructores" />
        <Manager category="Turnos" />
        <Manager category="Actividades" />
        <Manager category="Alumnos" />
        <Manager category="Equipamiento" />
        <button onClick={() => {} }>Ver Reportes</button>
    </div>
  );
}

export default Admin;