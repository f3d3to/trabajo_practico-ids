# HUELLAS A CASA

## Introducción

Este proyecto es un trabajo práctico para la materia Introducción al Desarrollo de Software. El objetivo es crear un sistema que resuelva un problema específico utilizando buenas prácticas de programación y metodologías ágiles.

## Descripción del Proyecto

Sitio web que permita publicar información sobre mascotas perdidas, utilizando google maps.
El sitio web debe permitir cargar mascotas que se perdieron, como así también tener un
buscador de mascotas por características, raza, color, condición, zona, barrio, etc. Las
publicaciones deben permitir cargar foto y geolocalizar en un mapa las mismas.
El sitio web debe informar si la mascota está en una casa de tránsito o dar alguna información
útil que se considere de importancia.
Por otra parte se deberá desarrollar una aplicación mobile que corra en android que cargue, la
información del animal, junto con una foto y geolocalización de la misma. Toda esta información
deberá aparecer una vez cargada en el sitio web.

### Listado de Endpoints de Servicios (API)

   - *POST /api/mascotas*
     - *Descripción:* Publicar una nueva mascota perdida.
     - *Datos de Entrada:* JSON con los datos de la mascota, incluyendo:
       - nombre: Nombre de la mascota.
       - especie: Especie de la mascota (perro, gato, otro).
       - raza: Raza de la mascota.
       - color: Color de la mascota.
       - condicion: Condición física (lastimada, sana).
       - zona y barrio: Zona y barrio específicos.
       - ubicacion: Ubicación geográfica (latitud y longitud).
       - foto: Archivo de imagen de la mascota.
       - estado: Estado (perdida, en tránsito, en adopción).
     - *Respuesta:* Confirmación de creación y id de la mascota.
     - *Método:* POST

   - *GET /api/mascotas/{id}*
     - *Descripción:* Obtener detalles de una mascota específica.
     - *Parámetros de Ruta:* id (ID de la mascota).
     - *Respuesta:* JSON con información detallada de la mascota.
     - *Método:* GET

   - *PUT /api/mascotas/{id}*
     - *Descripción:* Actualizar los datos de una mascota.
     - *Parámetros de Ruta:* id (ID de la mascota).
     - *Datos de Entrada:* JSON con los datos actualizados (estado, ubicación, etc.).
     - *Respuesta:* Confirmación de actualización.
     - *Método:* PUT

   - *DELETE /api/mascotas/{id}*
     - *Descripción:* Eliminar una publicación de mascota.
     - *Parámetros de Ruta:* id (ID de la mascota).
     - *Respuesta:* Confirmación de eliminación.
     - *Método:* DELETE

   - *GET /api/mascotas*
     - *Descripción:* Obtener todas las mascotas perdidas con filtros opcionales.
     - *Parámetros de Consulta:*
       - especie, raza, color, condicion, zona, barrio, estado.
     - *Respuesta:* JSON con la lista de mascotas que cumplen con los criterios de búsqueda.
     - *Método:* GET

   - *GET /api/mascotas/buscar*
     - *Descripción:* Búsqueda avanzada de mascotas según múltiples características.
     - *Parámetros de Consulta:*
       - Los mismos que el endpoint anterior para búsqueda específica.
     - *Respuesta:* JSON con la lista de mascotas encontradas.
     - *Método:* GET

   - *GET /api/mapa/mascotas*
     - *Descripción:* Obtener la ubicación de todas las mascotas para visualización en mapa.
     - *Parámetros de Consulta:*
       - zona: Filtro opcional por zona geográfica.
     - *Respuesta:* JSON con latitud y longitud de cada mascota perdida.
     - *Método:* GET

   - *POST /api/transito*
     - *Descripción:* Marcar una mascota como "en tránsito" en una casa temporal.
     - *Datos de Entrada:* JSON con:
       - id de la mascota, ubicacion_transito y informacion_contacto.
     - *Respuesta:* Confirmación de actualización.
     - *Método:* POST

   - *GET /api/transito*
     - *Descripción:* Obtener lista de mascotas en casas de tránsito.
     - *Parámetros de Consulta:* Opcional zona para filtro geográfico.
     - *Respuesta:* JSON con la lista de mascotas en estado de tránsito.
     - *Método:* GET

   - *POST /api/reportar-encontrado*
     - *Descripción:* Reportar que una mascota perdida fue encontrada.
     - *Datos de Entrada:* JSON con:
       - id de la mascota, ubicacion_encontrado, y informacion_contacto.
     - *Respuesta:* Confirmación del reporte.
     - *Método:* POST

   - *GET /api/preguntas*
     - *Descripción:* Obtener preguntas frecuentes y sus respuestas.
     - *Datos de Entrada:* N/A
     - *Respuesta:* JSON con preguntas frecuentes.
     - *Método:* GET

   - *POST /api/contacto*
     - *Descripción:* Enviar mensaje de contacto para soporte o consultas.
     - *Datos de Entrada:* JSON con nombre, email, y mensaje.
     - *Respuesta:* Confirmación de recepción.
     - *Método:* POST

## Requerimientos del Proyecto

    Uso de Github
    Uso de Docker (opcional)
    Utilización de un tablero Kanban con tareas a desarrollar (Backlog de producto)
    Creación de tres aplicaciones: front, mobile (Kivy (documentación)[https://kivy.org/doc/stable/])  y API
    API que se comunique con una base de datos MySQL
    Utilización de endpoints y formato JSON para el envío y recepción de información
    Utilización de una base de datos MySQL con al menos 2 tablas
    Realización de commits al repositorio con mensajes que incluyan el ID de la tarea correspondiente

## Hitos del Proyecto

- [X] Jueves 31/10: Entrega del Backlog de producto y mockup del sitio web
- [X] Jueves 7/11: Creación del repositorio y vistas del proyecto
- [ ] Jueves 14/11: Avances de la API y comunicación con el front
- [ ] Jueves 21/11: Integración de app mobile, front con API
- [ ] Jueves 28/11: 1er entrega del TP Integrador
- [ ] Martes 3/12: 2da entrega del TP integrador

##  Documentación Requerida

- [ ] Informe ([link al informe colaborativo](https://www.overleaf.com/3151471745zbgwysddhpxd#6e7d46))

    Carátula
    Integrantes
    Resumen
    Introducción
    Solución propuesta
    Tecnología utilizada
    Conclusión final

##  Condiciones de Aprobación

- [ ] No se debe utilizar variables globales, ciclos infinitos, código repetido, etc.
- [ ] Se debe evitar que el programa rompa frente a la interacción con el usuario
- [ ] Se debe modularizar el código y utilizar buenas prácticas de programación
- [ ] Se debe utilizar un repositorio en Github y entregar un programa que cumpla con la funcionalidad completa especificada

##  Fecha de Entrega
    El Trabajo Práctico cuenta con 2 fechas de entrega: 28/11/2024 y el 03/12/2024. Ambas tienen hora límite 18:00 hs.
