import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Carga variables del .env

def conectar_neon():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        print("¡Conexión exitosa a Neon!")
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# Ejemplo de consulta
with conectar_neon() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        print("Versión de PostgreSQL:", cur.fetchone()[0])
