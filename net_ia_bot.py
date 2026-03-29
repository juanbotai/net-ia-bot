from flask import Flask, request
import requests
import os
import threading
import time

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")

# 🔗 LINKS
LINK_REGISTRO = "https://4l.shop/KH0CY"
LINK_COMPRA = "https://4l.shop/MCRQ8"
LINK_EVALUACION = "https://4l.shop/WGPHR"
WHATSAPP = "https://wa.me/51976339774"

# 🔥 ESTADO USUARIO
estado_usuario = {}

# 🔥 ENVIAR BOTONES
def enviar_botones(chat_id, texto, opciones):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    teclado = {
        "keyboard": opciones,
        "resize_keyboard": True
    }

    requests.post(url, json={
        "chat_id": chat_id,
        "text": texto,
        "reply_markup": teclado
    })

# 🔥 SEGUIMIENTO AUTOMÁTICO
def seguimiento(chat_id):
    time.sleep(120)

    if chat_id in estado_usuario:
        enviar_botones(chat_id,
            f"""🔥 ¿Sigues interesado?

💪 Mejora tu salud  
💰 Genera ingresos  

📊 Haz tu evaluación:
{LINK_EVALUACION}

🛒 Compra:
{LINK_COMPRA}

🚀 Únete:
{LINK_REGISTRO}""",
            [["🛒 Comprar"], ["🚀 Unirme"], ["💬 Asesor"]]
        )

# 🔥 WEBHOOK
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
                [["💪 Salud"], ["💰 Negocio"]]
            )

        # 💪 SALUD PASO 1
        elif "salud" in texto:
            estado_usuario[chat_id] = "salud1"

            enviar_botones(chat_id,
                f"""💪 Vamos a mejorar tu salud

📊 Primero haz tu evaluación GRATIS:
{LINK_EVALUACION}

🔥 Te dirá exactamente qué necesitas

¿Ya hiciste la evaluación?""",
                [["✅ Ya lo hice"], ["📊 Hacer evaluación"]]
            )

        # 💪 SALUD PASO 2
        elif "ya" in texto and estado == "salud1":
            estado_usuario[chat_id] = "salud2"

            enviar_botones(chat_id,
                f"""🔥 Perfecto

Ahora sigue las recomendaciones

🛒 Compra aquí:
{LINK_COMPRA}

⏳ Mientras antes empieces, mejores resultados""",
                [["🛒 Comprar"], ["💬 Asesor"]]
            )

            threading.Thread(target=seguimiento, args=(chat_id,)).start()

        # 💪 REFORZAR EVALUACIÓN
        elif "evaluacion" in texto:
            enviar_botones(chat_id,
                f"""📊 Haz tu evaluación aquí:

{LINK_EVALUACION}

Luego regresa y te ayudo""",
                [["✅ Ya lo hice"]]
            )

        # 💰 NEGOCIO PASO 1
        elif "negocio" in texto or "dinero" in texto:
            estado_usuario[chat_id] = "negocio1"

            enviar_botones(chat_id,
                "💰 Excelente decisión\n\n¿Qué quieres lograr?",
                [["💵 Extra"], ["🚀 Grande"]]
            )

        # 💰 NEGOCIO PASO 2
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

            threading.Thread(target=seguimiento, args=(chat_id,)).start()

        # 🛒 COMPRA DIRECTA
        elif "comprar" in texto:
            enviar_botones(chat_id,
                f"""🛒 Compra aquí:

{LINK_COMPRA}

🔥 Empieza hoy""",
                [["💬 Asesor"]]
            )

        # 🚀 REGISTRO
        elif "unirme" in texto:
            enviar_botones(chat_id,
                f"""🚀 Regístrate aquí:

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
                [["💪 Salud"], ["💰 Negocio"]]
            )

    return "ok"

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
