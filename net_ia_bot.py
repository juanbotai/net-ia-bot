from flask import Flask, request
import requests
import sqlite3
from datetime import datetime
import os
import threading
import time

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔥 MEMORIA
historial = {}
estado_usuario = {}

def guardar_estado(chat_id, clave, valor):
    if chat_id not in estado_usuario:
        estado_usuario[chat_id] = {}
    estado_usuario[chat_id][clave] = valor

def obtener_estado(chat_id, clave):
    return estado_usuario.get(chat_id, {}).get(clave)

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
def enviar_imagen_ia(chat_id, prompt):
    imagen = generar_imagen_ia(prompt)

    if imagen:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

        requests.post(url, json={
            "chat_id": chat_id,
            "photo": imagen,
            "caption": "🔥 Imagen creada para ti"
        })
CONOCIMIENTO = """
4Life es una empresa internacional enfocada en salud y bienestar.

Muchas personas ya están mejorando su energía y generando ingresos.

Productos:
- Transfer Factor: fortalece el sistema inmunológico

Beneficios:
- Más energía diaria
- Mejor sistema inmune

Negocio:
- Ingresos desde casa
- Sistema duplicable

Frases clave:
- Puedes empezar hoy
- Muchas personas ya están viendo resultados
"""

# 🔥 INTENCIÓN
def detectar_intencion(texto):
    texto = texto.lower()

    if any(p in texto for p in ["precio", "cuanto", "costo", "comprar"]):
        return "caliente 🔥"
    elif any(p in texto for p in ["quiero", "me interesa", "negocio", "ingresos"]):
        return "caliente 🔥"
    elif any(p in texto for p in ["info", "que es", "como funciona"]):
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

# 🎥 VIDEO
def enviar_video(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"

    requests.post(url, json={
        "chat_id": chat_id,
        "video": "https://www.w3schools.com/html/mov_bbb.mp4",
        "caption": "🎥 Mira esto y dime qué te parece"
    })

# ⏱️ SEGUIMIENTO
def seguimiento(chat_id):
    time.sleep(60)
    enviar_botones(chat_id, "👀 Hola, ¿pudiste ver la info? Te ayudo a empezar 👍")

    time.sleep(120)
    enviar_botones(chat_id, "🔥 Muchas personas ya están logrando resultados… ¿quieres empezar?")

# 🔥 WEBHOOK
@app.route("/")
def home():
    return "Bot activo"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    texto = data["message"].get("text", "").strip()
    # 🔥 DETECTAR START (WEB / INTERESADO)
if texto.startswith("/start"):

    if "web" in texto:
    enviar_botones(
        chat_id,
        "🔥 Bienvenido\n\nEste sistema ya está ayudando a personas a generar ingresos desde su celular 📱💰\n\nDime… ¿buscas ingresos o mejorar tu salud?"
    )

    else:
        enviar_botones(chat_id, "🤖 Bienvenido\n\n¿Te interesa salud o negocio?")

    return "ok"   # 🔥 ESTA LÍNEA ES CLAVE

    texto_lower = texto.lower()

    # 🔥 GUARDAR INTERÉS

# 🔥 GUARDAR INTERÉS
if "salud" in texto_lower:
    guardar_estado(chat_id, "interes", "salud")

elif any(p in texto_lower for p in ["negocio", "dinero", "ingresos"]):
    guardar_estado(chat_id, "interes", "negocio")


# 🔥 IA VISUAL AUTOMÁTICA
if "salud" in texto_lower:
    prompt = "persona con energía, saludable, feliz, estilo vida fitness"
    enviar_imagen_ia(chat_id, prompt)

elif "negocio" in texto_lower:
    prompt = "persona trabajando desde casa con laptop, éxito financiero"
    enviar_imagen_ia(chat_id, prompt)    
        # 🔥 IA VISUAL AUTOMÁTICA
texto_lower = texto.lower()

# 🔥 GUARDAR INTERÉS
if "salud" in texto_lower:
    guardar_estado(chat_id, "interes", "salud")

elif any(p in texto_lower for p in ["negocio", "dinero", "ingresos"]):
    guardar_estado(chat_id, "interes", "negocio")


# 🔥 IA VISUAL AUTOMÁTICA
if "salud" in texto_lower:
    prompt = "persona con energía, saludable, feliz, estilo vida fitness"
    enviar_imagen_ia(chat_id, prompt)

elif "negocio" in texto_lower:
    prompt = "persona trabajando desde casa con laptop, éxito financiero"
    enviar_imagen_ia(chat_id, prompt)
        if "salud" in texto_lower:
    guardar_estado(chat_id, "interes", "salud")

    elif any(p in texto_lower for p in ["negocio", "dinero", "ingresos"]):
        guardar_estado(chat_id, "interes", "negocio")

    # 🔥 NIVEL
    nivel = detectar_intencion(texto)
    guardar_cliente(chat_id, nombre, texto, nivel)

    # 🔥 RESPUESTA
    if texto_lower == "salud 💪":
        respuesta = generar_respuesta(chat_id, "quiero mejorar mi salud", "salud")

    elif texto_lower == "negocio 💼":
        respuesta = generar_respuesta(chat_id, "quiero generar ingresos", "negocio")

    elif texto_lower == "comprar 🛒":
        respuesta = generar_respuesta(chat_id, "quiero comprar", "comprar")

    elif texto_lower == "info ℹ️":
        respuesta = generar_respuesta(chat_id, "quiero información", "info")
        enviar_video(chat_id)

    else:
        respuesta = generar_respuesta(chat_id, texto)

    # 🔥 CIERRE AUTOMÁTICO
    if nivel == "caliente 🔥":
        respuesta += "\n\n🔥 Estás a un paso… ¿empezamos hoy?"

    enviar_botones(chat_id, respuesta)

    # 🔥 SEGUIMIENTO
    if nivel != "frio ❄️":
        threading.Thread(target=seguimiento, args=(chat_id,)).start()

    return "ok"

# 🔥 IA
def generar_respuesta(chat_id, texto_usuario, tipo="general"):
    try:
        if chat_id not in historial:
            historial[chat_id] = []

        historial[chat_id].append({
            "role": "user",
            "content": texto_usuario
        })

        mensajes = historial[chat_id][-6:]

        # 🎯 MODO
        if tipo == "salud":
            modo = "Habla de beneficios de salud."
        elif tipo == "negocio":
            modo = "Habla de ingresos."
        elif tipo == "comprar":
            modo = "Cierra la venta."
        elif tipo == "info":
            modo = "Explica y genera interés."
        else:
            modo = "Detecta necesidad."

        # 🔥 PERSONALIZACIÓN POR INTERÉS
        interes = obtener_estado(chat_id, "interes")

        if interes == "salud":
            modo += " Enfócate en beneficios de salud."
        elif interes == "negocio":
            modo += " Enfócate en ingresos y libertad."

        # 🔥 PROMPT
        system_prompt = f"""
Eres NET, un experto CERRADOR de ventas de 4Life.

Conocimiento:
{CONOCIMIENTO}

Modo:
{modo}

Estrategia:
- Genera emoción
- Usa prueba social
- Lleva al cierre

Reglas:
- Máximo 3 líneas
- Termina con pregunta
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

        try:
            respuesta = result["output"][0]["content"][0]["text"]
        except:
            respuesta = "🔥 Tengo algo muy bueno para ti. ¿Buscas salud o ingresos?"

        historial[chat_id].append({
            "role": "assistant",
            "content": respuesta
        })

        texto_lower = texto_usuario.lower()

        # 🔥 CIERRE
        if any(p in texto_lower for p in ["quiero", "interesa", "comprar"]):
            respuesta += "\n\n🔥 ¿Empezamos hoy?"

        if "precio" in texto_lower:
            respuesta += "\n👉 https://wa.me/51976339774"

        if "negocio" in texto_lower:
            respuesta += "\n🚀 https://peru.4life.com/corp/signup/PC"

        return respuesta

    except Exception as e:
        print("ERROR IA:", e)
        return "⚠️ Error IA"

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
