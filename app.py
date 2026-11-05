import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "cambiar-esta-clave-secreta"
)

@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect(url_for("panel"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        if usuario and contrasena:
            flash("La conexión con MySQL se configurará en el siguiente paso.")
        else:
            flash("Ingresa tu usuario y contraseña.")

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
    return {"estado": "correcto", "sistema": "TECHESPINOZA"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
