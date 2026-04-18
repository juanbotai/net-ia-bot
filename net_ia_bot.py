
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    # Normalizar texto (evita errores con tildes)
    texto = update.message.text.lower().strip().replace("í", "i")

    if "si" in texto:
        await update.message.reply_text(
            "Perfecto 👌\n\n"
            "🔹 Aumentar ventas\n"
            "🔹 Automatizar clientes\n"
            "🔹 Mejorar productividad\n\n"
            "¿Cuál es tu mayor problema?"
        )

    elif "no" in texto:
        await update.message.reply_text(
            "Entiendo 👍\n\n"
            "Cuando quieras mejorar tu negocio, aquí estaré 💼🔥"
        )

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
    # Flask en segundo plano
    Thread(target=run_flask).start()

    # Bot en hilo principal (estable)
    run_bot()

if __name__ == "__main__":
    main()
