from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")

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

# 🔥 HOME
@app.route("/")
def home():
    return "Bot activo"

# 🔥 WEBHOOK
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    texto = data["message"].get("text", "").strip()

    # 🔥 START
    if texto.startswith("/start"):

        if "web" in texto:
            enviar_botones(chat_id, "🔥 Bienvenido desde la web\n\n¿Buscas ingresos o salud?")
        elif "interesado" in texto:
            enviar_botones(chat_id, "💰 Perfecto\n\n¿Cuánto te gustaría ganar al mes?")
        else:
            enviar_botones(chat_id, "🤖 Bienvenido\n\n¿Te interesa salud o negocio?")

        return "ok"

    # 🔥 RESPUESTA SIMPLE
    if "salud" in texto.lower():
        enviar_botones(chat_id, "💪 Te ayudo a mejorar tu salud\n\n¿Quieres más info?")
    elif "negocio" in texto.lower():
        enviar_botones(chat_id, "💰 Puedes generar ingresos desde casa\n\n¿Quieres empezar?")
    else:
        enviar_botones(chat_id, "🤖 Dime… ¿buscas salud o ingresos?")

    return "ok"

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
