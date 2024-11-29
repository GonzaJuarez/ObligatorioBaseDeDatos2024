import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children, allowedRoles }) => {
    const token = localStorage.getItem('access_token');
    const userRole = localStorage.getItem('user_role');

    // Verificar si el usuario está logueado
    if (!token) {
        // Si no hay token, redirigir al login
        return <Navigate to="/login" />;
    }

    // Verificar si el rol del usuario está dentro de los roles permitidos
    if (!allowedRoles.includes(parseInt(userRole))) {
        // Si el rol no está permitido, redirigir a una página de error o mostrar mensaje
        return <Navigate to="/alumnos" />;
    }

    // Si el usuario está logueado y tiene el rol adecuado, mostrar el contenido
    return children;
};

export default PrivateRoute;