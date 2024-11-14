# Proyecto Mascotas

Este proyecto está dividio en tres entornos: frotend, backend y mobile. A continuación se detallan los pasos para iniciar el proyecto en un entorno Docker, configurar el archivo `.env`, ver logs de cada contenedor y acceder a la base de datos.

## Requisitos Previos

- **Docker** y **Docker Compose** instalados en el sistema.

## Configuración del Entorno

### 1. Variables de Entorno

Copiar el archivo `.env.example` y renombrarlo a `.env`:

```bash
cp .env.example .env
```

En el archivo `.env`, seteás las variables. Por ejemplo:

```plaintext
# ENV BACKENDEND
BACKEND_PORT=5000
BACKEND_URL=http://backend

# DB env variables
DB_USER=db
DB_PASSWORD=db
DB_HOST=db
DB_PORT=3306
DB_NAME=db

# ENV DB
MYSQL_ROOT_PASSWORD=db
MYSQL_DATABASE=db
MYSQL_USER=db
MYSQL_PASSWORD=db

# ENV FRONTEND
FRONTEND_PORT=5001
```

### 2.

Para construir los "entornos" y "ejecutar" los contenedores:

```bash
docker compose up --build -d
```

Este comando se compone de :
- --build: para instalar todo los requisitos para que el proyecto funcione.
- -d: "detach", para poner el proceso en segundo plano, es decir no ver los logs de los contenedores.
- up: para ejecutar el proyecto.

### 3. Acceso a la Aplicación

Una vez que los contenedores estén "levantados", se accede con la url al frontend:

```
http://localhost:5000
```

## Comandos específicos

### Ver Logs de los Contenedores

Para ver los logs de un entorno en específico (por ejemplo del backend), usá el siguiente comando, reemplazando `nombre_servicio` con el nombre del servicio o [containername](https://docs.docker.com/reference/compose-file/services/#container_name) (en este caso `backend`, `frontend`, `db`):

Para ver logs del servicio en particular:
```bash
docker-compose logs -f <nombre_servicio>
```

Para ver todos los logs:

```bash
docker-compose logs -f
```

### Acceder a la db

Para acceder al contenedor de mysql (sustituir con los valores del .env):

```bash
docker-compose exec <nombre_servicio> psql -U $DB_USER -d $DB_NAME
```

Aclaración: abre una "línea de comandos" de mysql y se puede ejecutar comandos, por ejemplo `SELECT * FROM mascotas;`.

### Parar y Eliminar los Contenedores

Para detener ambos entornos del proyecto:

```bash
docker-compose down
```

*CUIDADO*. Este comando detiene el proyecto, pero *elimina* todos los elementos de la base de datos:

```bash
docker-compose down -v
```

## Consideraciones de Desarrollo

**Modificación del `.env`**: para editar las variables del `.env`, hay que reiniciar para que tome los nuevos valores (`down` y `up`).
