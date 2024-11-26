import React, { useState } from 'react';
import { TextField, Button, Typography, Alert, Box, Select, } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import '../Login/Login.css'
import { useNavigate } from 'react-router-dom';

const Signup = () => {
    return (
        <div>
            <Box className="login-box">
                <Typography variant="h4" component="h1" className="login-title">
                    Registro Usuarios
                </Typography>
                <form onSubmit={handleSubmit}>
                    <Box className="form-field">
                        <TextField
                            label="Email"
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
                    <Box className="form-field">
                        <TextField
                            label="Confirmar Password"
                            variant="outlined"
                            type="password"
                            fullWidth
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </Box>
                    <Box className="form-field">
                        <TextField
                            label="CI"
                            variant="outlined"
                            fullWidth
                            value={ci}
                            onChange={(e) => setCi(e.target.value)}
                            required
                        />
                    </Box>
                    <Box className="form-field">
                        <TextField
                            label="Nombre"
                            variant="outlined"
                            fullWidth
                            value={nombre}
                            onChange={(e) => setNombre(e.target.value)}
                            required
                        />
                    </Box>
                    <Box className="form-field">
                        <TextField
                            label="Apellido"
                            variant="outlined"
                            fullWidth
                            value={apellido}
                            onChange={(e) => setApellido(e.target.value)}
                            required
                        />
                    </Box>
                    <Box className="form-field">
                        <DatePicker
                            label="Fecha de Nacimiento"
                            value={fechaNacimiento}
                            onChange={(date) => setFechaNacimiento(date)}
                            renderInput={(params) => <TextField {...params} />}
                            required
                        />
                    </Box>
                    <Box className="form-field">
                        <Select
                            label="Rol"
                            variant="outlined"
                            fullWidth
                            value={rol}
                            onChange={(e) => setRol(e.target.value)}
                            required
                        >
                            <MenuItem value={1}>Administrador</MenuItem>
                            <MenuItem value={2}>Profesor</MenuItem>
                            <MenuItem value={3}>Alumno</MenuItem>
                        </Select>
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
                        Registrarse
                    </Button>
                </form>
            </Box>
        </div>
    );
}

export default Signup