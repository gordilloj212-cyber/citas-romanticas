from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB = "citas.db"

DIAS = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo"
]
HORAS = [f"{h:02d}:00" for h in range(10, 23)]
PLANES = [
    "🍿 Película juntos",
    "🍕 Cena romántica",
    "🌹 Paseo por el parque",
    "🍦 Ir por un helado",
    "💖 Una sorpresa"
]

with sqlite3.connect(DB) as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            dia TEXT,
            hora TEXT,
            plan TEXT
        )
    """)

PAGINA = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nuestra cita ❤️</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 20px;
    min-height: 100vh;
    display: grid;
    place-items: center;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg,#ffd6e7,#fff0f5);
    color: #873454;
}
.card {
    background: white;
    padding: 28px 22px;
    border-radius: 25px;
    width: 100%;
    max-width: 420px;
    text-align: center;
    box-shadow: 0 10px 35px #b52d5c25;
}
.heart { font-size: 55px; }
h1 { color: #e83e78; }
label {
    display: block;
    text-align: left;
    margin: 14px 0 6px;
    font-weight: bold;
}
input, select, button {
    width: 100%;
    padding: 13px;
    border-radius: 12px;
    font-size: 16px;
}
input, select {
    border: 1px solid #f0b6cb;
    background: white;
}
button {
    margin-top: 22px;
    border: 0;
    background: #f04480;
    color: white;
    font-weight: bold;
    cursor: pointer;
}
.mensaje {
    margin-top: 18px;
    padding: 12px;
    background: #fff0f5;
    border-radius: 12px;
}
</style>
</head>
<body>
<div class="card">
    <div class="heart">💖</div>
    <h1>¿Una cita conmigo?</h1>
    <p>Amor, elige cuándo nos vemos 🥰</p>

    <form method="POST">
        <label>Tu nombre</label>
        <input name="nombre" maxlength="60"
               placeholder="Tu nombre" required>

        <label>¿Qué día puedes?</label>
        <select name="dia" required>
            <option value="">Elige un día</option>
            {% for d in dias %}
            <option value="{{ d }}">{{ d }}</option>
            {% endfor %}
        </select>

        <label>¿A qué hora?</label>
        <select name="hora" required>
            <option value="">Elige una hora</option>
            {% for h in horas %}
            <option value="{{ h }}">{{ h }}</option>
            {% endfor %}
        </select>

        <label>¿Qué hacemos?</label>
        <select name="plan" required>
            <option value="">Elige nuestro plan</option>
            {% for p in planes %}
            <option value="{{ p }}">{{ p }}</option>
            {% endfor %}
        </select>

        <button type="submit">¡Confirmar nuestra cita! ❤️</button>
    </form>

    {% if mensaje %}
    <div class="mensaje">
        <h3>¡Qué ilusión! 💕</h3>
        <p>{{ mensaje }}</p>
    </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def inicio():
    mensaje = ""

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        dia = request.form.get("dia", "")
        hora = request.form.get("hora", "")
        plan = request.form.get("plan", "")

        if (
            nombre and dia in DIAS
            and hora in HORAS and plan in PLANES
        ):
            with sqlite3.connect(DB) as con:
                con.execute(
                    "INSERT INTO citas (nombre,dia,hora,plan) "
                    "VALUES (?,?,?,?)",
                    (nombre, dia, hora, plan)
                )
            mensaje = (
                f"{nombre}, ¡nos vemos el {dia} a las "
                f"{hora}! Plan: {plan}. ❤️"
            )

    return render_template_string(
        PAGINA, dias=DIAS, horas=HORAS,
        planes=PLANES, mensaje=mensaje
    )

if __name__ == "__main__":
    app.run(debug=False, port=5000)
