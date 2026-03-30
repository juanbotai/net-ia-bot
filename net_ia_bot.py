import os
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# =========================
# CONFIGURACIÓN
# =========================
TOKEN = os.getenv("TOKEN")  # Token seguro desde Render
PORT = int(os.environ.get("PORT", 10000))

# =========================
# FLASK PARA UPTIME
# =========================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot empresarial activo 24/7 💼🔥"

def run():
    app.run(host='0.0.0.0', port=PORT)

def keep_alive():
    t = Thread(target=run)
    t.start()

# =========================
# FUNCIONES BOT
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [["Sí", "No"]]
    await update.message.reply_text(
        "Hola 👋 Soy el asistente empresarial de Juan Quispe\n\n"
        "Ayudo a empresas a mejorar la energía, salud y productividad de sus trabajadores 💼\n\n"
        "¿Tu empresa tiene más de 5 colaboradores?",
        reply_markup=ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    # PASO 1: CALIFICACIÓN
    if "sí" in texto:
        teclado = [["Estrés", "Baja energía"], ["Enfermedades", "Rendimiento"]]
        await update.message.reply_text(
            "Perfecto 👌\n\n"
            "¿Cuál es el principal problema en tu equipo?",
            reply_markup=ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
        )

    elif "no" in texto:
        await update.message.reply_text(
            "Entiendo 👍\n\n"
            "Si en algún momento buscas mejorar la energía o salud de tu equipo, estaré aquí para ayudarte 💼"
        )

    # PASO 2: DETECCIÓN DE NECESIDAD
    elif texto in ["estrés", "baja energía", "enfermedades", "rendimiento"]:
        teclado = [["Agendar reunión", "Más información"]]
        await update.message.reply_text(
            "Excelente 👌\n\n"
            "Tenemos un programa empresarial que mejora eso
