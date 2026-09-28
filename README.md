# Examen Práctico Unidad I

Fundamentos de Arquitectura de Software y Desarrollo Backend
Alumno: Jesús Uc

Aquí está mi examen de la Unidad I. Son dos proyectos separados (una API REST y un servidor GraphQL) más las cinco preguntas teóricas.

## Estructura del repo

```
examen_rest/
  main.py
  database.py
  models.py
  requirements.txt
  Dockerfile
  compose.yaml
examen_graphql/
  schema.py
preguntas.txt
README.md
```

## Ejercicio 1: API REST con FastAPI, MySQL y Docker

API para el inventario de laptops del laboratorio. Las laptops se guardan en MySQL con SQLAlchemy, así que los datos siguen ahí aunque reinicie la API.

- `database.py`: conexión a MySQL (el host es `mysql`, que es el nombre del servicio en compose).
- `models.py`: la tabla `laptops`.
- `main.py`: la app, la carga inicial de 3 laptops (solo si la tabla está vacía) y los endpoints.
- `Dockerfile` y `compose.yaml`: levantan la API (`python:3.12-slim`) y MySQL 8.

Endpoints:

| Método | Ruta | Qué hace |
|--------|------|----------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/laptops` | Lista todas las laptops |
| GET | `/laptops/disponibles` | Solo las que tienen `disponible` en true |
| GET | `/laptops/{laptop_id}` | Una laptop, o 404 si no existe |
| POST | `/laptops` | Crea una laptop (queda disponible) |

Cómo correrlo (con Docker Desktop abierto):

```bash
cd examen_rest
docker compose up --build
```

La documentación queda en http://localhost:8000/docs. Para apagarlo:

```bash
docker compose down
```

Ojo: hay que apagarlo antes del ejercicio 2, porque los dos usan el puerto 8000.

## Ejercicio 2: Servidor GraphQL con Strawberry

Catálogo de talleres del laboratorio. Los talleres viven en una lista de Python en memoria, así que al detener el servidor vuelve a los tres iniciales.

- Tipos: `Instructor` y `Taller` (el instructor es un objeto anidado).
- Queries: `talleres`, `taller(nombre)` y `talleresActivos`.
- Mutation: `agregarTaller`, que recibe un input.

Cómo correrlo:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install "strawberry-graphql[cli]"
cd examen_graphql
strawberry dev schema
```

Se prueba en GraphiQL: http://localhost:8000/graphql

## Preguntas

Mis respuestas a las cinco preguntas teóricas están en [`preguntas.txt`](preguntas.txt).