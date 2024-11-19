const categoryConfig = {
    instructores: {
        create: [
            { key: 'nombre', label: 'Nombre', type: 'text' },
            { key: 'apellido', label: 'Apellido', type: 'text' },
            { key: 'ci', label: 'CI', type: 'text' },
        ],
        modify: [
            { key: 'ci', label: 'CI del Instructor a Modificar', type: 'text' },
            { key: 'nuevoNombre', label: 'Nuevo Nombre', type: 'text' },
            { key: 'nuevoApellido', label: 'Nuevo Apellido', type: 'text' },
        ],
        delete: [
            { key: 'ci', label: 'CI del Instructor a Eliminar', type: 'text' },
        ],
    },
    alumnos: {
        create: [
            { key: 'nombre', label: 'Nombre', type: 'text' },
            { key: 'apellido', label: 'Apellido', type: 'text' },
            { key: 'ci', label: 'CI', type: 'text' },
            { key: 'fechaNacimiento', label: 'Fecha de Nacimiento', type: 'date' },
        ],
        modify: [
            { key: 'ci', label: 'CI del Alumno a Modificar', type: 'text' },
            { key: 'nuevoNombre', label: 'Nuevo Nombre', type: 'text' },
            { key: 'nuevoApellido', label: 'Nuevo Apellido', type: 'text' },
        ],
        delete: [
            { key: 'ci', label: 'CI del Alumno a Eliminar', type: 'text' },
        ],
    },
    actividades: {
        create: [
            { key: 'descripcion', label: 'Descripción', type: 'text' },
            { key: 'costo', label: 'Costo de Alquiler', type: 'number' },
        ],
        modify: [
            { key: 'id', label: 'ID del Equipo a Modificar', type: 'text' },
            { key: 'nuevaDescripcion', label: 'Nueva Descripción', type: 'text' },
            { key: 'nuevoCosto', label: 'Nuevo Costo de Alquiler', type: 'number' },
        ],
        delete: [
            { key: 'id', label: 'ID del Equipo a Eliminar', type: 'text' },
        ],
    },
    turnos: {
        create: [
            { key: 'horaInicio', label: 'Hora de Inicio', type: 'time' },
            { key: 'horaFin', label: 'Hora de Fin', type: 'time' },
        ],
        modify: [
            { key: 'id', label: 'ID del Turno a Modificar', type: 'text' },
            { key: 'nuevaHoraInicio', label: 'Nueva Hora de Inicio', type: 'time' },
            { key: 'nuevaHoraFin', label: 'Nueva Hora de Fin', type: 'time' },
        ],
        delete: [
            { key: 'id', label: 'ID del Turno a Eliminar', type: 'text' },
        ],
    }
};

export default categoryConfig;