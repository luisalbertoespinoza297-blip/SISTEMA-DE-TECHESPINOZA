import os
import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "techespinoza_db"),
            port=int(os.getenv("DB_PORT", "3306"))
        )
        return conexion

    except Error as error:
        print(f"Error de conexión MySQL: {error}")
        return None
