from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.commands import start, registrar, registrar_datos
from handlers.messages import manejar_mensaje
from db.models import create_tables

def main():
    create_tables()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", registrar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_datos))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    print("NutriBot funcionando...")
    app.run_polling()

if __name__ == '__main__':
    main()
