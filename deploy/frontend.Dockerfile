# frontend.Dockerfile
FROM python:3.10-slim

# Definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt y realizar la instalación de dependencias
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Copiar el código del frontend al contenedor
COPY ../frontend /app

# Exponer el puerto del frontend
EXPOSE 5001

# Comando para iniciar la aplicación frontend
CMD ["python", "app.py"]
