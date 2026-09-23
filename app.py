from flask import Flask, render_template, request, redirect, make_response, url_for, session

app = Flask(__name__)
app.secret_key = "NvJ+7O?I34VXTs77£0$9"


usuarios = {
    "carlos": "1111",
    "laura": "2222",
    "diego": "3333"
}

libros = [
    {"titulo": "Python desde cero", "autor": "Juan Pérez", "disponibles": 4},
    {"titulo": "Desarrollo Web", "autor": "María López", "disponibles": 2},
    {"titulo": "Inteligencia Artificial", "autor": "Pedro García", "disponibles": 0}
]

@app.route("/")
def index():
    ultimo_usuario = request.cookies.get("ultimo_usuario")
    mensaje_logout = session.pop("mensaje_logout", None)
    return render_template("index.html", ultimo_usuario=ultimo_usuario, mensaje_logout=mensaje_logout)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contrasena = request.form.get("contrasena")

        if usuario in usuarios and usuarios[usuario] == contrasena:
            session["usuario"] = usuario
            respuesta = make_response(redirect(url_for("libros_view")))
            respuesta.set_cookie("ultimo_usuario", usuario, max_age=60 * 60 * 24 * 30)
            session["mensaje_bienvenida"] = f"Bienvenido, {usuario}."
            return respuesta
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("login.html", error=error)


@app.route("/libros")
def libros_view():
    mensaje_bienvenida = session.pop("mensaje_bienvenida", None)
    return render_template("libros.html", libros=libros, mensaje_bienvenida=mensaje_bienvenida)


@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("perfil.html", usuario=session["usuario"])


@app.route("/logout")
def logout():
    session.clear()
    session["mensaje_logout"] = "Sesión cerrada"
    return redirect(url_for("index"))

@app.route("/eliminar_cookie")
def eliminar_cookie():
    respuesta = make_response(redirect(url_for("index")))
    respuesta.delete_cookie("ultimo_usuario")
    return respuesta

if __name__ == "__main__":
    app.run(debug=True, port=5011)
