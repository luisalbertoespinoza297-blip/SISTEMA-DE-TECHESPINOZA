from werkzeug.security import generate_password_hash
from conexion import obtener_conexion


def crear_administrador():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar con MySQL.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        usuario = "admin"
        contrasena = "CambiarAdmin2026!"

        clave = generate_password_hash(contrasena)

        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (usuario,)
        )

        if cursor.fetchone():
            print("El administrador ya existe.")
            return

        cursor.execute(
            """
            INSERT INTO usuarios (usuario, contrasena, rol)
            VALUES (%s, %s, %s)
            """,
            (usuario, clave, "administrador")
        )

        conexion.commit()
        print("Administrador creado correctamente.")

    except Exception as error:
        print(f"Error: {error}")

    finally:
        if cursor:
            cursor.close()
        conexion.close()


if __name__ == "__main__":
    crear_administrador()
