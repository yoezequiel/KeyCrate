import string
import random
from flask import Flask, render_template, request, session, redirect
from config import SECRET_KEY
from favicon import get as get_favicon
import sqlite3
import hashlib
from urllib.parse import urlparse

app = Flask(__name__)
app = Flask(__name__, static_url_path="/static")
app.secret_key = SECRET_KEY

def render_html(template_name: str, **context):
    if not template_name.endswith(".html"):
        template_name += ".html"
    return render_template(template_name, **context)


def get_db_connection():
    conn = sqlite3.connect("KeyCrate.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sitio TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )
    conn.commit()
    conn.close()


def generate_password(length, numbers, letters, symbols):
    password_characters = ""
    if numbers:
        password_characters += string.digits
    if letters:
        password_characters += string.ascii_letters
    if symbols:
        password_characters += string.punctuation

    return "".join(random.choice(password_characters) for i in range(int(length)))


@app.route("/")
def index():
    return render_html("index")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password = request.form["password"]
        if not username or not password:
            return render_html(
                "registro",
                error="El nombre de usuario y/o la contraseña no pueden estar vacíos.",
            )
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user:
            conn.close()
            return render_html(
                "registro",
                error="El nombre de usuario ya está en uso. Por favor, elije otro.",
            )
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        session["user_id"] = user["id"]
        conn.close()
        return redirect("/menu")
    return render_html("registro")


@app.route("/inicio_sesion", methods=["GET", "POST"])
def inicio_sesion():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password),
        ).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            return redirect("/menu")
        return render_html(
            "inicio_sesion", error="Nombre de usuario o contraseña incorrectos."
        )
    return render_template("inicio_sesion.html")


@app.route("/recuperar_contraseña", methods=["GET", "POST"])
def recuperar_contraseña():
    if request.method == "POST":
        username = request.form["username"]
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        if user:
            return render_html(
                "recuperar_contraseña",
                success="Se ha enviado un correo electrónico con la contraseña.",
            )
        return render_html(
            "recuperar_contraseña",
            error="No se encontró ningún usuario con ese nombre de usuario.",
        )
    return render_html("recuperar_contraseña")


@app.route("/menu")
def menu():
    if "user_id" in session:
        conn = get_db_connection()
        user_id = session["user_id"]
        rows = conn.execute(
            "SELECT * FROM passwords WHERE user_id = ?", (user_id,)
        ).fetchall()
        conn.close()
        passwords = []
        for row in rows:
            password = dict(row)
            domain = password["sitio"]
            logo_keyword = None
            if "google" in domain:
                logo_keyword = "google"
            elif "facebook" in domain:
                logo_keyword = "facebook"
            elif "amazon" in domain:
                logo_keyword = "amazon"
            elif "dropbox" in domain:
                logo_keyword = "dropbox"
            elif "linkedin" in domain:
                logo_keyword = "linkedin"
            elif "microsoft" in domain:
                logo_keyword = "microsoft"
            elif "netflix" in domain:
                logo_keyword = "netflix"
            elif "twitter" in domain:
                logo_keyword = "twitter"
            elif "youtube" in domain:
                logo_keyword = "youtube"
            if logo_keyword:
                logo_path = f"static/img/logos/{logo_keyword}.webp"
                password["logo_path"] = logo_path
            else:
                password["logo_path"] = ""
            passwords.append(password)
        return render_html("mostrar_contraseñas", passwords=passwords)
    return redirect("/inicio_sesion")


@app.route("/profile")
def profile():
    if "user_id" in session:
        return render_html("profile")
    else:
        return render_html("index")


@app.route("/agregar_contraseña", methods=["GET", "POST"])
def agregar_contraseña():
    if "user_id" in session:
        if request.method == "POST":
            sitio = request.form["sitio"]
            username = request.form["username"]
            password = request.form["password"]
            if not sitio or not username or not password:
                return render_html(
                    "agregar_contraseña",
                    error="Todos los campos son obligatorios y no pueden estar vacíos.",
                )
            conn = get_db_connection()
            user_id = session["user_id"]
            conn.execute(
                "INSERT INTO passwords (user_id, sitio, username, password) VALUES (?, ?, ?, ?)",
                (user_id, sitio, username, password),
            )
            conn.commit()
            conn.close()
            return redirect("/menu")
        return render_html("agregar_contraseña")
    return redirect("/inicio_sesion")


@app.route("/eliminar_contraseña/<int:password_id>", methods=["POST"])
def eliminar_contraseña_id(password_id):
    if "user_id" in session:
        conn = get_db_connection()
        user_id = session["user_id"]
        conn.execute(
            "DELETE FROM passwords WHERE id = ? AND user_id = ?", (password_id, user_id)
        )
        conn.commit()
        conn.close()
    return redirect("/menu")


@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.pop("user_id", None)
    return redirect("/inicio_sesion")


@app.route("/eliminar_cuenta")
def eliminar_cuenta():
    if "user_id" in session:
        return redirect("/confirmar_eliminacion")
    return redirect("/inicio_sesion")


@app.route("/del_cuenta")
def del_cuenta():
    if "user_id" in session:
        conn = get_db_connection()
        user_id = session["user_id"]
        conn.execute("DELETE FROM passwords WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        session.pop("user_id", None)
        return redirect("/registro")
    return redirect("/inicio_sesion")


@app.route("/confirmar_eliminacion", methods=["GET", "POST"])
def confirmar_eliminacion():
    if request.method == "POST":
        confirmation = request.form.get("confirmation")
        if confirmation == "eliminar":
            return redirect("/del_cuenta")
        return redirect("/profile")
    return render_html("confirmar_eliminacion")


@app.route("/generar_contraseña", methods=["GET", "POST"])
def generar_contraseña():
    message = ""
    password = ""
    MAX_LENGTH = 80

    if request.method == "POST":
        try:
            length = int(request.form.get("length", 8))  # Longitud por defecto 8
            length = max(4, min(length, MAX_LENGTH))

            useNumbers = request.form.get("numbers") == "on"
            useLetters = request.form.get("letters") == "on"
            useSymbols = request.form.get("symbols") == "on"

            if not (useNumbers or useLetters or useSymbols):
                message = ("Por favor, seleccione al menos una opción para generar la contraseña.")
            else:
                password = generate_password(length, useNumbers, useLetters, useSymbols)
                
        except ValueError:
            message = ("Por favor, ingrese una longitud valida.")

    return render_html("generar_contraseña", message=message, password=password)



@app.errorhandler(404)
def page_not_found(error):
    return render_html("404"), 40


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))
