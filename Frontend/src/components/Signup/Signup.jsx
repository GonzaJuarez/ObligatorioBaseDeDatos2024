import React, { useState } from 'react';
import { TextField, Button, Typography, Box, Alert, Select } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './Signup.css';


const Signup = () => {
    const [formData, setFormData] = useState({
        ci: '',
        id_rol: 1,
        nombre: '',
        apellido: '',
        fechaNacimiento: '',
        cel: '',
        correo: '',
        password: '',
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    // Manejar cambios en los campos de texto
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    // Manejar el envío del formulario de registro
    const handleSignupSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess(false);

        try {
            // Crear la persona en la base de datos
            const personaResponse = await fetch('http://localhost:8000/personas', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ci: formData.ci,
                    id_rol: formData.id_rol,  // Cambié 'formData.rol' por 'formData.id_rol'
                    nombre: formData.nombre,
                    apellido: formData.apellido,
                    fecha_nacimiento: formData.fechaNacimiento,
                    cel: formData.cel,
                    correo: formData.correo,
                }),
            });

            if (!personaResponse.ok) {
                throw new Error('Error al crear la persona');
            }

            // Crear el login para la persona
            const loginResponse = await fetch('http://localhost:8000/login/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    correo: formData.correo,
                    contrasena: formData.password,
                }),
            });

            if (!loginResponse.ok) {
                throw new Error('Error al crear el login');
            }

            // Si ambas solicitudes tienen éxito, proceder al inicio de sesión
            await handleLogin();
        } catch (error) {
            console.error('Error:', error);
            setError('Registro fallido. Por favor, intente de nuevo.');
        }
    };

    // Función para iniciar sesión automáticamente después del registro
    const handleLogin = async () => {
        try {
            const response = await fetch('http://localhost:8000/login/confirm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    correo: formData.correo,
                    contrasena: formData.password,
                }),
            });

            if (!response.ok) {
                throw new Error('Error al iniciar sesión');
            }

            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user_role', data.rol);

            setSuccess(true);
            if ([1, 2].includes(data.rol)) {
                navigate('/admin');
            } else {
                navigate('/alumnos');
            }
        } catch (error) {
            console.error('Error:', error);
            setError('Error al iniciar sesión automáticamente.');
        }
    };

    return (
        <Box className="signup-box">
            <Typography variant="h4" component="h1" className="signup-title">
                Registro de Usuario
            </Typography>
            <form onSubmit={handleSignupSubmit}>
                <Box className="form-field">
                    <TextField
                        label="Correo"
                        name="correo"
                        variant="outlined"
                        fullWidth
                        value={formData.correo}
                        onChange={handleChange}
                        required
                    />
                </Box>
                <Box className="form-field">
                    <TextField
                        label="contraseña"
                        name="password"
                        variant="outlined"
                        type="password"
                        fullWidth
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </Box>
                <Box className="form-field">
                    <TextField
                        label="Nombre"
                        name="nombre"
                        variant="outlined"
                        fullWidth
                        value={formData.nombre}
                        onChange={handleChange}
                        required
                    />
                </Box>
                <Box className="form-field">
                    <TextField
                        label="Apellido"
                        name="apellido"
                        variant="outlined"
                        fullWidth
                        value={formData.apellido}
                        onChange={handleChange}
                        required
                    />
                </Box>
                <Box className="form-field">
                    <TextField
                        label="Cédula de Identidad"
                        name="ci"
                        variant="outlined"
                        fullWidth
                        value={formData.ci}
                        onChange={handleChange}
                        required
                    />
                </Box>
                <Box className="form-field">
                    <TextField
                        label="Fecha de Nacimiento"
                        name="fechaNacimiento"
                        type="date"
                        variant="outlined"
                        fullWidth
                        InputLabelProps={{
                            shrink: true,
                        }}
                        value={formData.fechaNacimiento}
                        onChange={handleChange}
                        required
                    />
                </Box>
                <Box className="form-field">
                    <TextField
                        label="Celular"
                        name="cel"
                        variant="outlined"
                        fullWidth
                        value={formData.cel}
                        onChange={handleChange}
                        required
                    />
                </Box>
                <Box className="form-field">
                    <Select
                        native
                        variant="outlined"
                        fullWidth
                        name="id_rol"  // Cambié el nombre a "id_rol" para que coincida con el objeto formData
                        value={formData.id_rol}
                        onChange={handleChange}
                        required
                    >
                        <option value={1}>Administrador</option>
                        <option value={2}>Profesor</option>
                        <option value={3}>Alumno</option>
                    </Select>
                </Box>
                {error && (
                    <Box className="form-field">
                        <Alert severity="error">{error}</Alert>
                    </Box>
                )}
                {success && (
                    <Box className="form-field">
                        <Alert severity="success">Registro exitoso, redirigiendo...</Alert>
                    </Box>
                )}
                <Button type="submit" variant="contained" fullWidth>
                    Registrarse
                </Button>
            </form>
        </Box>
    );
};

export default Signup;
