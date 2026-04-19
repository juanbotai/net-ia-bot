import os
import nest_asyncio
from flask import Flask
from threading import Thread

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

# 🔥 Evita errores de async
nest_asyncio.apply()

# 🔐 TOKEN (mejor usar variable de entorno en Render)
TOKEN = os.getenv("TOKEN")

# 🌐 Flask (para Render)
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot activo en Render 🚀"


# =========================
# 🤖 LÓGICA DEL BOT
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola 👋\n\n"
        "Soy tu asistente inteligente 🤖\n\n"
        "¿Quieres mejorar tu negocio?\n\n"
        "Responde:\n"
        "👉 SI\n"
        "👉 NO"
    )


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    texto = (
        update.message.text
        .lower()
        .strip()
        .replace("í", "i")
    )

    # 🔥 RESPUESTAS INTELIGENTES
    if any(p in texto for p in ["si", "sí", "ok", "claro", "quiero"]):
        await update.message.reply_text(
            "Perfecto 👌\n\n"
            "🔹 Aumentar ventas\n"
            "🔹 Automatizar clientes\n"
            "🔹 Mejorar productividad\n\n"
            "👉 ¿Cuál es tu mayor problema?\n\n"
            "1️⃣ Ventas\n"
            "2️⃣ Tiempo\n"
            "3️⃣ Clientes"
        )

    elif any(p in texto for p in ["no", "nop", "negativo"]):
        await update.message.reply_text(
            "Entiendo 👍\n\n"
            "💼 Cuando quieras mejorar tu negocio, aquí estaré 🔥"
        )

    elif texto == "1":
        await update.message.reply_text(
            "🔥 Te ayudo a aumentar tus ventas con automatización.\n\n"
            "¿Te gustaría ver cómo funciona?"
        )

    elif texto == "2":
        await update.message.reply_text(
            "⏳ Vamos a automatizar tu tiempo con un bot inteligente.\n\n"
            "¿Quieres una demo?"
        )

    elif texto == "3":
        await update.message.reply_text(
            "📈 Podemos generar clientes automáticamente para ti.\n\n"
            "¿Quieres empezar?"
        )

    else:
        await update.message.reply_text(
            "👇 Responde con:\n"
            "SI / NO\n"
            "o elige una opción (1, 2, 3)"
        )


# =========================
# 🚀 INICIAR BOT
# =========================

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("🤖 Bot activo...")
    app_bot.run_polling()


# =========================
# 🔥 MAIN
# =========================

def main():
    # Ejecutar bot en segundo plano
    Thread(target=run_bot).start()

    # Flask en puerto de Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
