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
# 🔥 ESTADO USUARIO
estado_usuario = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"].get("text", "").lower()

        estado = estado_usuario.get(chat_id, "inicio")

        # 🚀 INICIO
        if texto == "/start":
            estado_usuario[chat_id] = "inicio"

            enviar_botones(chat_id,
                "🔥 Bienvenido a 4Life\n\n¿Qué deseas hoy?",
                [["🔥 Salud"], ["💰 Negocio"]]
            )

        # 💪 SALUD (PASO 1)
        elif "salud" in texto:
            estado_usuario[chat_id] = "salud1"

            enviar_botones(chat_id,
                "💪 Perfecto\n\n¿Qué deseas mejorar?",
                [["⚡ Energía"], ["🛡️ Sistema Inmune"]]
            )

        # 💪 SALUD (PASO 2)
        elif estado == "salud1":
            estado_usuario[chat_id] = "salud2"

            enviar_botones(chat_id,
                f"""🔥 Este producto es ideal

✔ Más energía  
✔ Defensas altas  

🛒 Compra aquí:
{LINK_COMPRA}

⏳ Oferta limitada""",
                [["🛒 Comprar Ahora"], ["💬 Asesor"]]
            )

        # 💰 NEGOCIO (PASO 1)
        elif "negocio" in texto:
            estado_usuario[chat_id] = "negocio1"

            enviar_botones(chat_id,
                "💰 Perfecto\n\n¿Qué buscas?",
                [["💵 Extra"], ["🚀 Grande"]]
            )

        # 💰 NEGOCIO (PASO 2)
        elif estado == "negocio1":
            estado_usuario[chat_id] = "negocio2"

            enviar_botones(chat_id,
                f"""🔥 Este negocio es para ti

✔ Ingresos desde casa  
✔ Sistema probado  

🚀 Únete aquí:
{LINK_REGISTRO}

⏳ Cupos limitados""",
                [["🚀 Unirme"], ["💬 Asesor"]]
            )

        # 🛒 COMPRA FINAL
        elif "comprar" in texto:
            enviar_botones(chat_id,
                f"""🛒 Compra ahora

{LINK_COMPRA}

🔥 Empieza hoy mismo""",
                [["💬 Asesor"]]
            )

        # 🚀 REGISTRO FINAL
        elif "unirme" in texto:
            enviar_botones(chat_id,
                f"""🚀 Regístrate ahora

{LINK_REGISTRO}

💼 Empieza hoy""",
                [["💬 Asesor"]]
            )

        # 💬 WHATSAPP
        elif "asesor" in texto:
            enviar_botones(chat_id,
                f"""💬 Escríbeme aquí:

{WHATSAPP}

Te guío paso a paso""",
                [["🔥 Inicio"]]
            )

        # 🔁 RESET
        else:
            estado_usuario[chat_id] = "inicio"

            enviar_botones(chat_id,
                "🔥 Elige una opción",
                [["🔥 Salud"], ["💰 Negocio"]]
            )

    return "ok"

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
