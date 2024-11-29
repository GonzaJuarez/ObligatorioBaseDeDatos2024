import React from 'react'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import PrivateRoute from './components/PrivateRoute/PrivateRoute.jsx'
import Login from './components/Login/Login.jsx'
import Alumnos from './components/Alumnos/Alumnos.jsx'
import Admin from './components/Admin/Admin.jsx'
import Reportes from './components/Reportes/Reportes.jsx'
import Signup from './components/Signup/Signup.jsx'
import './App.css'

function App() {

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/alumnos" element={<Alumnos />} />
          <Route path="/admin/reportes" element={<Reportes />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="*" element={<Navigate to="/login" />} />
          <Route
            path="/admin"
            element={
              <PrivateRoute allowedRoles={[1, 2]}>
                <Admin />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/reportes"
            element={
              <PrivateRoute allowedRoles={[1, 2]}>
                <Reportes />
              </PrivateRoute>
            }
          />


        </Routes>
        <ToastContainer />
      </Router>
    </div>
  )

}

export default App
