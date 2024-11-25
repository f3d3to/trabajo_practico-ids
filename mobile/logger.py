import logging

# Configuración del logger
logging.basicConfig(
    filename="appLog.log",   # Guardar los logs en 'loggings.txt'
    filemode="w",              # Modo 'a' para añadir los logs (no sobrescribir)
    level=logging.DEBUG,       # Nivel de logging: DEBUG para capturar todos los detalles
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato de log
)

# Crear un logger específico para la aplicación
logger = logging.getLogger("MyApp")
