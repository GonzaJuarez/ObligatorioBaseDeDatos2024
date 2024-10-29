# ObligatorioBaseDeDatos2024
- - - -
## Api

---
### Tecnologias
* Python 3.13 <br>
* FastAPI <br>
* SQLAlchemy <br>
* MySQL <br>
* Docker <br>

### Instalación
1. Clonar el repositorio:
```
git clone https://github.com/GonzaJuarez/ObligatorioBaseDeDatos2024.git
```
2. Abrir Docker Desktop <br><br>
3. Abrir la carpeta base del proyecto en una terminal <br><br>
4. Moverse a la carpeta DataBase:
```
cd DataBase
```
5. Buildear el contenedor de Docker:
```
docker-compose build
```
6. Levantar el contenedor de Docker:
```
docker-compose up
```
7. Abrir la carpeta base del proyecto en otra terminal <br><br>
8. Crear un entorno virtual:
```
python -m venv env 
```
9. Activar el entorno virtual:
```
env\Scripts\activate
```
10. Instalar las dependencias:
```
pip install -r requirements.txt
```
11. Moverse a la carpeta Api:
```
cd Api
```
12. Levantar el servidor:
```
uvicorn app:app --reload
```

### Endpoints

---

#### Actividades
* **Get:** /actividades 
```
Muestra todas las actividades
```
* **Get:** /actividades/{id}
```
> Muestra la actividad con el {id}
```
* **Post:** /actividades 
```
Crea una nueva actividad
{
    "id": "id",
    "descripcion": "descripcion",
    "equipamiento": "equipamiento"
}
```
* **Put:** /actividades/{id}
```
> Modifica la actividad con el {id}
{
    "id": "id",
    "descripcion": "descripcion",
    "equipamiento": "equipamiento"
}
```
* **Delete:** /actividades/{id}
```
Elimina la actividad con el {id}
```

---

#### Alumno por clase
* **Get:** /alumno_clase
```
Muestra todos los alumnos por clases
```
* **Get:** /alumno_clase/{id}
```
> Muestra los alumnos por clase con el {id}
```
* **Post:** /alumno_clase 
```
Crea un nuevo alumno por clase
{
    "id_clase": "id_clase",
    "id_alumno": "id_alumno",
    "id_equipamiento": "id_equipamiento"
}
```
* **Put:** /alumno_clase/{id}
```
Modifica el alumno por clase con el {id}
{
    "id_clase": "id_clase",
    "id_alumno": "id_alumno",
    "id_equipamiento": "id_equipamiento"
}
```
* **Delete:** /alumno_clase/{id} 
```
Elimina el alumno por clase con el {id}
```

---

#### Clase
* **Get:** /clase
```
Muestra todas las clases
```
* **Get:** /clase/{id}
```
Muestra la clase con el {id} 
```
* **Post:** /clase 
```
Crea una nueva clase
{
    "id": "id",
    "id_instructor": "id_instructor",
    "id_actividad": "id_actividad",
    "id_turno": "id_turno",
    "dictada": "dictada"
}
```
* **Put:** /clase/{id} 
```
Modifica la clase con el {id}
{
    "id": "id",
    "id_instructor": "id_instructor",
    "id_actividad": "id_actividad",
    "id_turno": "id_turno",
    "dictada": "dictada"
}
```
* **Delete:** /clase/{id} 
```
Elimina la clase con el {id}
```

---

#### Equipamiento
* **Get:** /equipamiento
```
Muestra todos los equipamientos}
```
* **Get:** /equipamiento/{id}
```
Muestra el equipamiento con el {id}
```
* **Post:** /equipamiento 
```
Crea un nuevo equipamiento
{
    "id": "id",
    "id_actividad": "id_actividad",
    "descripcion": "descripcion",
    "costo": "costo"
}
```
* **Put:** /equipamiento/{id} 
```
Modifica el equipamiento con el {id}
{
    "id": "id",
    "id_actividad": "id_actividad",
    "descripcion": "descripcion",
    "costo": "costo"
}
```
* **Delete:** /equipamiento/{id}
```
Elimina el equipamiento con el {id}
```

---

#### Login
* **Get:** /login
```
Muestra todos los logins
```
* **Get:** /login/{ci}
```
Muestra el login con el {ci}
```
* **Post:** /login 
```
Crea un nuevo login
{
    "ci": "ci",
    "contraseña": "contraseña"
}
```
* **Put:** /login/{ci} 
```
Modifica el login con el {ci}
{
    "ci": "ci",
    "contraseña": "contraseña"
}
```
* **Delete:** /login/{ci} 
```
Elimina el login con el {ci}
```

---

#### Personas
* **Get:** /personas <br>
```
Muestra todas las personas
```
* **Get:** /personas/{ci} <br>
``` 
Muestra la persona con el {ci}
```
* **Post:** /personas
```
Crea una nueva persona
{
    "ci": "ci",
    "id_rol": "id_rol",
    "nombre": "nombre",
    "apellido": "apellido",
    "fecha_nacimiento": "fecha_nacimiento",
    "cel": "cel",
    "correo": "correo"
}
```
* **Put:** /personas/{ci} 
```
Modifica la persona con el {ci}
{
    "ci": "ci",
    "id_rol": "id_rol",
    "nombre": "nombre",
    "apellido": "apellido",
    "fecha_nacimiento": "fecha_nacimiento",
    "cel": "cel",
    "correo": "correo"
}
```
* **Delete:** /personas/{ci} 
```
Elimina la persona con el {ci}
```

---

#### Roles
* **Get:** /roles
```
Muestra todos los roles
```
* **Get:** /roles/{id}
```
Muestra el rol con el {id}
```
* **Post:** /roles 
```
Crea un nuevo rol
{
    "id": "id",
    "descripcion": "descripcion"
}
```
* **Put:** /roles/{id} 
```
Modifica el rol con el {id}
{
    "id": "id",
    "descripcion": "descripcion"
}
```
* **Delete:** /roles/{id} 
```
Elimina el rol con el {id}
```

---

#### Turnos
* **Get:** /turno
```
Muestra todos los turnos 
```
* **Get:** /turno/{id}
```
Muestra el turno con el {id}
```
* **Post:** /turno 
```
Crea un nuevo turno
{
    "id": "id",
    "hora_inicio": "hora_inicio",
    "hora_fin": "hora_fin"
}
```
* **Put:** /turno/{id}
```
Modifica el turno con el {id}
{
    "id": "id",
    "hora_inicio": "hora_inicio",
    "hora_fin": "hora_fin"
}
```
* **Delete:** /turno/{id} 
```
Elimina el turno con el {id}
```

- - - -

## Integrantes
* Juan Pablo Cerizola
* Agustin Muniz
* Gonzalo Juarez
