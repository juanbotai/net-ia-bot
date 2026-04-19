import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "TU_TOKEN_AQUI"

app = Flask(__name__)

# Ruta básica para Render
@app.route("/")
def home():
    return "Bot activo correctamente"

# Función del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy tu bot activo 🚀")

# Función para correr el bot
def run_bot():
    import asyncio

    async def main():
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        await application.run_polling()

    asyncio.run(main())

# Ejecutar bot en segundo plano
Thread(target=run_bot).start()
