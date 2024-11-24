const roleIds = {
    administrador: 1,
    instructor: 2,
    alumno: 3,
  };
  

const categoryConfig = {

    instructores: {
        create: [
            { key: 'ci', label: 'CI', type: 'number' },
            { key: 'nombre', label: 'Nombre', type: 'text' },
            { key: 'apellido', label: 'Apellido', type: 'text'},
            { key: 'fecha_nacimiento', label: 'Fecha de Nacimiento', type: 'date' },
            { key: 'cel', label: 'Cel', type: 'number'},
            { key: 'correo', label: 'Correo', type: 'text'},
        ],
        roleId: roleIds.instructor,
        modify: [
            { key: 'ci', label: 'CI del Instructor a Modificar', type: 'text' },
            { key: 'nombre', label: 'Nombre', type: 'text' },
            { key: 'apellido', label: 'Apellido', type: 'text'},
            { key: 'fecha_nacimiento', label: 'Fecha de Nacimiento', type: 'date' },
            { key: 'cel', label: 'Cel', type: 'number'},
            { key: 'correo', label: 'Correo', type: 'text'},
        ],
        delete: [
            { key: 'ci', label: 'CI del Instructor a Eliminar', type: 'text' },
        ],
    },
    alumnos: {
        create: [
            { key: 'ci', label: 'CI', type: 'number' },
            { key: 'nombre', label: 'Nombre', type: 'text' },
            { key: 'apellido', label: 'Apellido', type: 'text'},
            { key: 'fecha_nacimiento', label: 'Fecha de Nacimiento', type: 'date' },
            { key: 'cel', label: 'Cel', type: 'number'},
            { key: 'correo', label: 'Correo', type: 'text'},
            { idrol: '3'}
        ],
        roleId: roleIds.instructor,
        modify: [
            { key: 'ci', label: 'CI del Alumno a Modificar', type: 'text' },
            { key: 'nombre', label: 'Nombre', type: 'text' },
            { key: 'apellido', label: 'Apellido', type: 'text'},
            { key: 'fecha_nacimiento', label: 'Fecha de Nacimiento', type: 'date' },
            { key: 'cel', label: 'Cel', type: 'number'},
            { key: 'correo', label: 'Correo', type: 'text'},
        ],
        delete: [
            { key: 'ci', label: 'CI del Alumno a Eliminar', type: 'text' },
        ],
    },
    actividades: {
        create: [
            { key: 'descripcion', label: 'Descripción', type: 'text' },
            { key: 'costo', label: 'Costo', type: 'number' },
        ],
        modify: [
            { key: 'id', label: 'ID de la Actividad', type: 'text' },
            { key: 'descripcion', label: 'Descripción', type: 'text' },
            { key: 'costo', label: 'Costo', type: 'number' },
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
            { key: 'id', label: 'ID del Turno', type: 'text' },
            { key: 'nuevaHoraInicio', label: 'Hora de Inicio', type: 'time' },
            { key: 'nuevaHoraFin', label: 'Hora de Fin', type: 'time' },
        ],
        delete: [
            { key: 'id', label: 'ID del Turno a Eliminar', type: 'text' },
        ],
    }
};

export default categoryConfig;