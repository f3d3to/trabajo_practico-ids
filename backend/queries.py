from . import engine
from sqlalchemy import text

QUERY_TODAS_LAS_MASCOTAS = ""
QUERY_MASCOTA_BY_ID = ""
QUERY_INSERTAR_MASCOTA = ""
QUERY_ACTUALIZAR_MASCOTA = ""
QUERY_BORRAR_MASCOTA = ""

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    return result

def todas_mascotas():
    return run_query(QUERY_TODAS_LAS_MASCOTAS).fetchall()

def mascota_by_id(id):
    return run_query(QUERY_MASCOTA_BY_ID, {'id': id}).fetchall()

def insertar_mascota(data):
    run_query(QUERY_INSERTAR_MASCOTA, data)

def actualizar_mascota(id, data):
    run_query(QUERY_ACTUALIZAR_MASCOTA, {'id': id, **data})

def borrar_mascota(id):
    run_query(QUERY_BORRAR_MASCOTA, {'id': id})
