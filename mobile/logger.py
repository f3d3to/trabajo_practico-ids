import logging

def setup_logger(log_file="appLog.log", log_level=logging.DEBUG):
    """
    Configura y devuelve un logger para la aplicación.
    """
    logging.basicConfig(
        filename=log_file,           # Especifica el archivo de log
        filemode="w",                # Modo 'w' para sobrescribir
        level=log_level,             # Establece el nivel de log
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato
    )

    logger = logging.getLogger("MyApp")
    return logger

# Configuración del logger
logger = setup_logger()
