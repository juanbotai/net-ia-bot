from flask import Flask, request
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

import os

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# 🔥 MEMORIA
historial = {}

# 🔥 BASE DE DATOS
def iniciar_db():
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        chat_id TEXT PRIMARY KEY,
        nombre TEXT,
        interes TEXT,
        nivel TEXT,
        fecha TEXT
    )
    """)

    conn.commit()
    conn.close()

iniciar_db()

# 🔥 GUARDAR CLIENTE
def guardar_cliente(chat_id, nombre, interes, nivel):
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute("""
    INSERT OR REPLACE INTO clientes VALUES (?, ?, ?, ?, ?)
    """, (chat_id, nombre, interes, nivel, fecha))

    conn.commit()
    conn.close()

# 🔥 CONOCIMIENTO
def cargar_conocimiento():
    try:
        with open("conocimiento.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

CONOCIMIENTO = cargar_conocimiento()

# 🔥 INTENCIÓN
def detectar_intencion(texto):
    texto = texto.lower()

    if any(p in texto for p in ["precio", "cuanto", "costo"]):
        return "caliente 🔥"
    elif any(p in texto for p in ["quiero", "me interesa"]):
        return "caliente 🔥"
    elif any(p in texto for p in ["info", "que es"]):
        return "medio 😐"
    else:
        return "frio ❄️"

# 🔥 BOTONES
def enviar_botones(chat_id, texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    botones = {
        "keyboard": [
            ["Salud 💪", "Negocio 💼"],
            ["Comprar 🛒", "Info ℹ️"]
        ],
        "resize_keyboard": True
    }

    requests.post(url, json={
        "chat_id": chat_id,
        "text": texto,
        "reply_markup": botones
    })

# 🔥 WEBHOOK
@app.route("/")
def home():
    return "Bot activo"
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return "ok"

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"].get("text", "")
        nombre = data["message"]["chat"].get("first_name", "cliente")

        nivel = detectar_intencion(texto)
        guardar_cliente(chat_id, nombre, texto, nivel)

        # BOTONES CON IA
        if texto.lower() == "salud 💪":
            respuesta = generar_respuesta(chat_id, "quiero mejorar mi salud", "salud")

        elif texto.lower() == "negocio 💼":
            respuesta = generar_respuesta(chat_id, "quiero generar ingresos", "negocio")

        elif texto.lower() == "comprar 🛒":
            respuesta = generar_respuesta(chat_id, "quiero comprar", "comprar")

        elif texto.lower() == "info ℹ️":
            respuesta = generar_respuesta(chat_id, "quiero información", "info")

        else:
            respuesta = generar_respuesta(chat_id, texto)

        enviar_botones(chat_id, respuesta)

    return "ok"

# 🔥 IA REAL
def generar_respuesta(chat_id, texto_usuario, tipo="general"):
    try:
        if chat_id not in historial:
            historial[chat_id] = []

        historial[chat_id].append({
            "role": "user",
            "content": texto_usuario
        })

        mensajes = historial[chat_id][-6:]

        # 🎯 MODO SEGÚN BOTÓN
        modo = ""
        if tipo == "salud":
            modo = "Habla de beneficios de salud."
        elif tipo == "negocio":
            modo = "Habla de ingresos y oportunidad."
        elif tipo == "comprar":
            modo = "Cierra la venta."
        elif tipo == "info":
            modo = "Explica y genera interés."
        else:
            modo = "Detecta necesidad y guía."

        system_prompt = f"""
Eres NET, experto en ventas de 4Life.

Conocimiento:
{CONOCIMIENTO}

Modo:
{modo}

Reglas:
- Máx 3 líneas
- Termina con pregunta
- Lenguaje humano
"""

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4o-mini",
            "input": [
                {"role": "system", "content": system_prompt},
                *mensajes
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers=headers,
            json=data
        )

        result = response.json()
        print("STATUS:", response.status_code)
        print("IA RESPONSE:", result)

        # 🔥 LECTURA SEGURA
        try:
            respuesta = result["output"][0]["content"][0]["text"]
        except:
            respuesta = "🤖 Estoy procesando... intenta otra vez"

        historial[chat_id].append({
            "role": "assistant",
            "content": respuesta
        })

        texto_lower = texto_usuario.lower()

        # 🔥 WHATSAPP
        if any(p in texto_lower for p in ["precio", "comprar", "interesa"]):
            respuesta += "\n\n👉 Escríbeme: https://wa.me/51976339774"

        # 🔥 AFILIACIÓN
        if any(p in texto_lower for p in [
            "afiliarme", "registrarme", "inscribirme",
            "quiero entrar", "negocio", "unirme"
        ]):
            respuesta += "\n\n🚀 Regístrate aquí:\nhttps://peru.4life.com/corp/signup/PC"

        return respuesta

    except Exception as e:
        print("ERROR IA:", e)
        return "⚠️ Error IA"

# 🔥 DASHBOARD
@app.route("/crm")
def dashboard():
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes ORDER BY fecha DESC")
    datos = cursor.fetchall()

    conn.close()

    total = len(datos)
    calientes = len([c for c in datos if "caliente" in c[3]])

    html = f"""
    <html>
    <body style="background:#0f172a;color:white;text-align:center;font-family:Arial">
    <h1>🚀 CRM NIVEL DIOS</h1>
    <h3>Total: {total} | Calientes: {calientes}</h3>
    <table border=1 style="margin:auto;width:90%">
    <tr><th>Nombre</th><th>Interés</th><th>Nivel</th><th>Fecha</th></tr>
    """

    for c in datos:
        html += f"<tr><td>{c[1]}</td><td>{c[2]}</td><td>{c[3]}</td><td>{c[4]}</td></tr>"

    html += "</table></body></html>"
    return html

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
