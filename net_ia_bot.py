import os
import nest_asyncio
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

nest_asyncio.apply()

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot activo 💼🔥"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

# ===== BOT =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [["Sí", "No"]]
    await update.message.reply_text(
        "Hola 👋 Soy el asistente empresarial\n\n¿Tu empresa tiene más de 5 colaboradores?",
        reply_markup=ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if "si" in texto or "sí" in texto:
        await update.message.reply_text("Perfecto 👌 ¿Qué problema tienes?")

    elif "no" in texto:
        await update.message.reply_text("Entiendo 👍 Escríbeme cuando quieras mejorar tu negocio")

    else:
        await update.message.reply_text("Usa los botones 👇")

# ===== RUN =====

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot activo 🚀")
    app_bot.run_polling()

def main():
    Thread(target=run_flask).start()
    Thread(target=run_bot).start()

if __name__ == "__main__":
    main()import os
import nest_asyncio
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# =========================
# FIX ASYNC
# =========================
nest_asyncio.apply()

# =========================
# CONFIG
# =========================
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 10000))

# =========================
# FLASK (OBLIGATORIO EN RENDER)
# =========================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot empresarial activo 24/7 💼🔥"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

# =========================
# BOT TELEGRAM
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [["Sí", "No"]]
    await update.message.reply_text(
        "Hola 👋 Soy el asistente empresarial de Juan Quispe\n\n"
        "Ayudo a empresas a mejorar energía ⚡ salud 💪 y productividad 📈\n\n"
        "¿Tu empresa tiene más de 5 colaboradores?",
        reply_markup=ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if any(p in texto for p in ["sí", "si"]):
        teclado = [["Estrés", "Baja energía"], ["Enfermedades", "Rendimiento"]]
        await update.message.reply_text(
            "Perfecto 👌\n\n¿Cuál es el principal problema en tu equipo?",
            reply_markup=ReplyKeyboardMarkup(teclado, resize_keyboard=True)
        )

    elif "no" in texto:
        await update.message.reply_text(
            "Entiendo 👍\n\nCuando quieras mejorar la salud o productividad de tu equipo, escríbeme 💼"
        )

    elif any(p in texto for p in ["estrés", "estres", "baja energía", "energia", "enfermedades", "rendimiento"]):
        teclado = [["Agendar reunión", "Más información"]]
        await update.message.reply_text(
            "Excelente 👌\n\nTenemos un programa empresarial que soluciona ese problema 📈🔥\n\n¿Qué deseas hacer?",
            reply_markup=ReplyKeyboardMarkup(teclado, resize_keyboard=True)
        )

    elif "agendar" in texto:
        await update.message.reply_text(
            "Perfecto 🚀\n\nAgenda aquí tu reunión directa conmigo:\n"
            "👉 https://wa.me/51976339774\n\n"
            "Te ayudaré personalmente 💼🔥"
        )

    elif "información" in texto or "informacion" in texto:
        await update.message.reply_text(
            "Claro 👇\n\nNuestro programa mejora:\n"
            "✅ Energía del equipo\n"
            "✅ Sistema inmunológico\n"
            "✅ Rendimiento laboral\n\n"
            "Trabajamos con tecnología de transferencia de factores 🌐\n\n"
            "¿Te gustaría una presentación personalizada?"
        )

    else:
        await update.message.reply_text(
            "👉 Por favor usa los botones para continuar"
        )

# =========================
# EJECUCIÓN PARA RENDER
# =========================

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot Telegram activo 🚀")
    app_bot.run_polling(drop_pending_updates=True)

def main():
    # Flask en hilo separado
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Bot en hilo separado
    bot_thread = Thread(target=run_bot)
    bot_thread.start()

    print("Sistema completo activo 🔥")

if __name__ == "__main__":
    main()
