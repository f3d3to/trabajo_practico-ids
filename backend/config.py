from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Verificación de variables de entorno
if not all([os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME')]):
    raise ValueError("Algunas variables de entorno para la conexión a la base de datos están incompletas.")

# Configuración de la conexión a la base de datos
DATABASE_URI = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URI)
