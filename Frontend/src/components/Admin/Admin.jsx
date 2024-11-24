import React from 'react';
import Manager from '../Manager/Manager';
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
        <button onClick={() => window.location.href = "/Admin/Reportes"}>Ver Reportes</button>
    </div>
  );
}

export default Admin;