# Guía para deployar localhost con Ngrok

Este instructivo detalla los pasos para instalar y configurar Ngrok, obtener el token de autenticación y desplegar simultáneamente dos aplicaciones locales utilizando una única sesión de agente.

## Instalación de Ngrok

1. Descarga el binario de Ngrok desde la página: [https://ngrok.com/download](https://ngrok.com/download).
2. Descomprimi el archivo:
   tar -xvzf ngrok-v3-stable-linux-amd64.tgz
3. Mové el binario extraído a `/usr/local/bin` para que esté disponible globalmente:
   sudo mv ngrok /usr/local/bin/
4. Verifica que Ngrok esté instalado correctamente ejecutando:
   ngrok version

## Configuración inicial

1. Registrate en Ngrok en [https://ngrok.com/signup](https://ngrok.com/signup) y accede a tu cuenta.
2. Copiá tu token de autenticación desde el dashboard en [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken).
3. Agregá el token de autenticación a tu configuración local ejecutando:
   `ngrok config add-authtoken TU_AUTHTOKEN`\
   Reemplazá TU_AUTHTOKEN con el token que copiaste.

## Configuración de múltiples túneles (frontend y backend)

1. Ubica o crea el archivo de configuración de Ngrok:
   - En Linux/Mac: `~/.config/ngrok/ngrok.yml`
   - (CHEQUEAR POR LAS DUDAS)En Windows: `%HOMEPATH%\AppData\Local\ngrok\ngrok.yml`
2. Editaá el archivo de configuración para definir los túneles necesarios. Por ejemplo, exponer el backend en el puerto 5000 y el frontend en el puerto 5001:
```yml
   version: "2"
   authtoken: TU_AUTHTOKEN
   tunnels:
     backend:
       proto: http
       addr: 5000
     frontend:
       proto: http
       addr: 5001
```
   Reemplazá  `TU_AUTHTOKEN` por tu token.

## Desplegar múltiples aplicaciones

1. Iniciá ambos túneles simultáneamente desde una única sesión de Ngrok ejecutando:
   `ngrok start --all`
2. Ngrok generará URLs públicas para cada túnel configurado. Por ejemplo:
   - Backend: https://`<UUID>`.ngrok-free.app → redirige a localhost:5000
   - Frontend: https://`<UUID>`.ngrok-free.app → redirige a localhost:5001

## CUIDADO CON EL SITIO QUE GENERAR PQ ESTÁS EXPONIENDO TU MAQUINA A TODO INTERNET
