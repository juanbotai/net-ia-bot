import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 🔐 TOKEN
TOKEN = os.getenv("TOKEN")

# 🌐 Flask
app = Flask(__name__)

# 🤖 Crear bot
app_bot = ApplicationBuilder().token(TOKEN).build()


# =========================
# 🚀 RUTA PRINCIPAL
# =========================
@app.route("/")
def home():
    return "🤖 Bot activo en webhook 🚀"


# =========================
# 🤖 COMANDO START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola 👋\n\n"
        "Soy tu asistente inteligente 🤖\n\n"
        "¿Quieres mejorar tu negocio?\n\n"
        "👉 SI\n👉 NO"
    )


# =========================
# 🤖 RESPUESTAS
# =========================
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    texto = update.message.text.lower().strip()

    print("Mensaje recibido:", texto)

    if any(p in texto for p in ["si", "sí", "ok", "claro", "quiero"]):
        await update.message.reply_text(
            "Perfecto 👌\n\n"
            "🔹 Aumentar ventas\n"
            "🔹 Automatizar clientes\n"
            "🔹 Mejorar productividad\n\n"
            "👉 ¿Cuál es tu mayor problema?\n\n"
            "1️⃣ Ventas\n2️⃣ Tiempo\n3️⃣ Clientes"
        )

    elif any(p in texto for p in ["no", "nop", "negativo"]):
        await update.message.reply_text(
            "Entiendo 👍\n\n"
            "💼 Cuando quieras, aquí estaré 🔥"
        )

    elif texto == "1":
        await update.message.reply_text(
            "🔥 Te ayudo a aumentar ventas automáticamente.\n\n¿Quieres ver cómo?"
        )

    elif texto == "2":
        await update.message.reply_text(
            "⏳ Automatiza tu tiempo con bots inteligentes.\n\n¿Te muestro?"
        )

    elif texto == "3":
        await update.message.reply_text(
            "📈 Genera clientes en automático.\n\n¿Empezamos?"
        )

    else:
        await update.message.reply_text(
            "👇 Responde:\nSI / NO o 1, 2, 3"
        )


# =========================
# 🔥 CONFIGURAR BOT
# =========================
async def setup_bot():
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    await app_bot.initialize()
    await app_bot.start()


# Ejecutar setup una sola vez
asyncio.run(setup_bot())


# =========================
# 🌐 WEBHOOK
# =========================
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json()
    update = Update.de_json(data, app_bot.bot)

    await app_bot.process_update(update)
    return "ok"
