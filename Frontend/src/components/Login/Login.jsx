import React, { useState } from 'react';
import { TextField, Button, Typography, Alert, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './Login.css';  // Importa el archivo CSS

const Login = () => {
    const [correo, setCorreo] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('http://localhost:8000/login/confirm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ correo, contraseña: password }),
            });

            if (!response.ok) {
                throw new Error('Login fallido');
            }

            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user_role', data.rol); // Almacenar el rol del usuario

            setError('');
            if ([1, 2].includes(data.rol)) {
                navigate('/admin');
            } else {
                navigate('/alumnos');
            }
            
            
        } catch (error) {
            console.error('Error:', error);
            setError('Login fallido. Verifica tus credenciales.');
        }
    };

    const handleRegisterRedirect = () => {
        navigate('/signup');
    };

    return (
        <div>
            <Box className="login-box">
                <Typography variant="h4" component="h1" className="login-title">
                    Winter Games Login
                </Typography>
                <form onSubmit={handleSubmit}>
                    <Box className="form-field">
                        <TextField
                            label="Correo"
                            variant="outlined"
                            fullWidth
                            value={correo}
                            onChange={(e) => setCorreo(e.target.value)}
                            required
                        />
                    </Box>
                    <Box className="form-field">
                        <TextField
                            label="Contraseña"
                            variant="outlined"
                            type="password"
                            fullWidth
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </Box>
                    {error && (
                        <Box className="form-field">
                            <Alert severity="error">{error}</Alert>
                        </Box>
                    )}
                    <Button
                        type="submit"
                        variant="contained"
                        fullWidth
                        className="login-button"
                    >
                        Ingresar
                    </Button>
                    <Button
                        variant="text"
                        fullWidth
                        className="register-button"
                        onClick={handleRegisterRedirect}
                        sx={{
                            backgroundColor: 'transparent',
                            '&:hover': {
                              backgroundColor: 'transparent', 
                              color: '#115293', 
                            },
                          }}
                    >
                        ¿No tenés cuenta? Registrate
                    </Button>
                </form>
            </Box>
        </div>
    );
}

export default Login;
