import React, { useState } from 'react';
import { TextField, Button, Typography, Alert, Box } from '@mui/material';
import backgroundImage from './login.jpg';
import './Login.css';  // Importa el archivo CSS

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            console.log('Login successful:', data);
            setError('');
        } catch (error) {
            console.error('Error:', error);
            setError('Login failed. Please check your credentials and try again.');
        }
    };

    return (
        <div className="login-background">
            <Box className="login-box">
                <Typography variant="h4" component="h1" className="login-title">
                    Winter Games Login
                </Typography>
                <form onSubmit={handleSubmit}>
                    <Box className="form-field">
                        <TextField
                            label="Username"
                            variant="outlined"
                            fullWidth
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </Box>
                    <Box className="form-field">
                        <TextField
                            label="Password"
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
                        Login
                    </Button>
                </form>
            </Box>
        </div>
    );
};

export default Login;
