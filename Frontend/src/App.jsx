import React from 'react'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Login/Login.jsx'
import Alumnos from './components/Alumnos/Alumnos.jsx'
import Profesores from './components/Profesores/Profesores.jsx'
import Admin from './components/Admin/Admin.jsx'
import './App.css'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/Login"/>}/>
        <Route path="/login" element={<Login />} />
        <Route path="/alumnos" element={<Alumnos />} />
        <Route path="/profesores" element={<Profesores />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
      <ToastContainer />
    </Router>
  )
    
}

export default App
