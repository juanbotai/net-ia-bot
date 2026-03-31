import os
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# =========================
# CONFIGURACIÓN
# =========================
TOKEN = os.getenv("TOKEN")  # Token desde Render
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
        "Ayudo a empresas a mejorar la energía, salud y productividad 💼\n\n"
        "¿Tu empresa tiene más de 5 colaboradores?",
        reply_markup=ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    # PASO 1
    if "sí" in texto:
        teclado = [["Estrés", "Baja energía"], ["Enfermedades", "Rendimiento"]]
        await update.message.reply_text(
            "Perfecto 👌\n\n"
            "¿Cuál es el principal problema en tu equipo?",
            reply_markup=ReplyKeyboardMarkup(teclado, resize_keyboard=True)
        )

    elif "no" in texto:
        await update.message.reply_text(
            "Entiendo 👍\n\n"
            "Si en algún momento deseas mejorar la salud o productividad de tu equipo, escríbeme 💼"
        )

    # PASO 2
    elif texto in ["estrés", "baja energía", "enfermedades", "rendimiento"]:
        teclado = [["Agendar reunión", "Más información"]]
        await update.message.reply_text(
            "Excelente 👌\n\n"
            "Tenemos un programa empresarial que mejora ese problema 📈\n\n"
            "¿Qué deseas hacer?",
            reply_markup=ReplyKeyboardMarkup(teclado, resize_keyboard=True)
        )

    # PASO 3 - CIERRE
    elif "agendar" in texto:
        await update.message.reply_text(
            "Perfecto 🚀\n\n"
            "Agenda aquí tu reunión directa conmigo:\n"
            "👉 https://wa.me/51976339774\n\n"
            "Te ayudaré personalmente 💼🔥"
        )

    elif "más información" in texto:
        await update.message.reply_text(
            "Claro 👇\n\n"
            "Nuestro programa mejora:\n"
            "✅ Energía del equipo\n"
            "✅ Sistema inmunológico\n"
            "✅ Rendimiento laboral\n\n"
            "Trabajamos con tecnología de transferencia de factores 🌐\n\n"
            "¿Te gustaría una presentación personalizada?"
        )

    else:
        await update.message.reply_text(
            "No entendí 🤖\n\n"
            "Por favor usa los botones para continuar."
        )

# =========================
# INICIO BOT
# =========================

def main():
    keep_alive()

    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot empresarial corriendo 24/7 🚀")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
