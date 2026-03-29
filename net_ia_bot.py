from flask import Flask, request
import requests
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")

# 🔗 LINKS
LINK_REGISTRO = "https://4l.shop/KH0CY"
LINK_COMPRA = "https://4l.shop/MCRQ8"
WHATSAPP = "https://wa.me/51976339774"

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

# 🔥 BOTONES
def enviar_botones(chat_id, texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    botones = {
        "keyboard": [
            ["🔥 Salud", "💰 Negocio"],
            ["🛒 Comprar", "🚀 Unirme"]
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

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"].get("text", "").lower()
        nombre = data["message"]["chat"].get("first_name", "cliente")

        guardar_cliente(chat_id, nombre, texto, "activo")

        # 🚀 INICIO
        if texto == "/start":
            respuesta = f"""🔥 Bienvenido a 4Life

💪 Mejora tu salud
💰 Genera ingresos

👉 Empieza aquí:
{LINK_REGISTRO}

Elige una opción 👇"""

        # 💪 SALUD
        elif "salud" in texto:
            respuesta = f"""💪 Mejora tu salud con 4Life

✔ Más energía  
✔ Sistema inmune fuerte  
✔ Mejor bienestar  

🛒 Compra aquí:
{LINK_COMPRA}

💬 Escríbeme:
{WHATSAPP}"""

        # 💰 NEGOCIO
        elif "negocio" in texto or "dinero" in texto:
            respuesta = f"""💰 Genera ingresos con 4Life

✔ Gana comisiones  
✔ Negocio internacional  
✔ Sin jefes  

🚀 Únete aquí:
{LINK_REGISTRO}

💬 Escríbeme:
{WHATSAPP}"""

        # 🛒 COMPRAR
        elif "comprar" in texto:
            respuesta = f"""🛒 Compra productos 4Life

🔥 Resultados reales

👉 Compra aquí:
{LINK_COMPRA}

💬 Escríbeme:
{WHATSAPP}"""

        # 🚀 UNIRME
        elif "unirme" in texto or "inscrib" in texto:
            respuesta = f"""🚀 Únete al equipo 4Life

💼 Empieza hoy  
💪 Mejora tu vida  

👉 Regístrate:
{LINK_REGISTRO}

💬 Escríbeme:
{WHATSAPP}"""

        # ❗ CONTROL TOTAL
        else:
            respuesta = """🔥 Elige una opción:

💪 Salud  
💰 Negocio  
🛒 Comprar  
🚀 Unirme  

👇 Usa los botones"""

        enviar_botones(chat_id, respuesta)

    return "ok"

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
