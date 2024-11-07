# backend.Dockerfile
FROM python:3.10-slim

# Definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt y realizar la instalación de dependencias
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Copiar el código del backend al contenedor
COPY ../backend /app

# Exponer el puerto del backend
EXPOSE 5000

# Comando para iniciar la aplicación backend
CMD ["python", "app.py"]
