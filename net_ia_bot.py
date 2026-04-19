from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "TU_TOKEN_AQUI"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo 🚀"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola Juan, tu bot está funcionando 🔥")

# Ejecutar bot correctamente
async def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Bot iniciado...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()  # 👈 IMPORTANTE

# Hilo para Render
def start_bot():
    asyncio.run(run_bot())

Thread(target=start_bot).start()
