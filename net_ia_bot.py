import os
import nest_asyncio
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Fix async
nest_asyncio.apply()

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 10000"))

# Flask
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
    if not update.message or not update.message.text:
        return

    texto = update.message.text.lower().strip()

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
    main()
