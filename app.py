
import os
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import check_password_hash
from conexion import obtener_conexion
from mysql.connector import Error

app = Flask(__name__, template_folder="plantillas")

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "clave-temporal-cambiar-en-ethiodeploy"
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax"
)


@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect(url_for("panel"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario" in session:
        return redirect(url_for("panel"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        if not usuario or not contrasena:
            flash("Ingresa tu usuario y contraseña.")
            return render_template("login.html")

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                flash("No se pudo conectar con la base de datos.")
                return render_template("login.html")

            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    u.id,
                    u.nombre,
                    u.usuario,
                    u.password_hash,
                    u.estado,
                    r.nombre AS rol
                FROM usuarios u
                INNER JOIN roles r ON u.rol_id = r.id
                WHERE u.usuario = %s
                LIMIT 1
            """

            cursor.execute(consulta, (usuario,))
            cuenta = cursor.fetchone()

            if cuenta is None:
                flash("Usuario o contraseña incorrectos.")

            elif cuenta["estado"] != "Activo":
                flash("Tu cuenta está desactivada.")

            elif check_password_hash(
                cuenta["password_hash"], contrasena
            ):
                session["usuario"] = cuenta["usuario"]
                session["nombre"] = cuenta["nombre"]
                session["rol"] = cuenta["rol"]
                session["usuario_id"] = cuenta["id"]

                return redirect(url_for("panel"))

            else:
                flash("Usuario o contraseña incorrectos.")

        except (Error, ValueError) as error:
            print(f"Error en el inicio de sesión: {error}")
            flash("Ocurrió un problema al verificar tus datos.")

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    return render_template("login.html")


@app.route("/panel")
def panel():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("panel.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/salud")
def salud():
    return {
        "estado": "correcto",
        "sistema": "TECHESPINOZA"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
