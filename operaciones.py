from conexion import obtener_conexion


def listar_equipos():
    conexion = obtener_conexion()
    if conexion is None:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipos ORDER BY id DESC")
        equipos = cursor.fetchall()
        return equipos
    except Exception as error:
        print(f"Error al listar equipos: {error}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def buscar_equipo(id_equipo):
    conexion = obtener_conexion()
    if conexion is None:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM equipos WHERE id = %s",
            (id_equipo,)
        )
        return cursor.fetchone()
    except Exception as error:
        print(f"Error al buscar equipo: {error}")
        return None
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
