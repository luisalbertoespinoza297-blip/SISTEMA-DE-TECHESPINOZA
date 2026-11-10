
import os
import mysql.connector
from urllib.parse import urlparse, unquote
from mysql.connector import Error


def obtener_conexion():
    try:
        database_url = os.environ.get("DATABASE_URL")

        if not database_url:
            raise ValueError("No se encontró DATABASE_URL")

        datos = urlparse(database_url)

        conexion = mysql.connector.connect(
            host=datos.hostname,
            port=datos.port or 3306,
            user=unquote(datos.username or ""),
            password=unquote(datos.password or ""),
            database=datos.path.lstrip("/"),
            connection_timeout=10
        )

        return conexion

    except (Error, ValueError) as error:
        print(f"Error de conexión MySQL: {error}")
        return None
