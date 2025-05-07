import logging
from telegram import Update  # Importa la clase Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes, CallbackQueryHandler
from config import BOT_TOKEN
from handlers.commands import (
    registrar, recibir_nombre, recibir_edad, recibir_peso,
    recibir_altura, recibir_objetivo, recibir_metas, manejar_alergias,  # Agregar recibir_alergias
    cancelar, recomendacion_recetas, contar_calorias, salir, manejar_alergias  # Agregar manejar_alergias
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy NutriBot 🤖\nEstoy conectado y listo para ayudarte.")

def main():
    app = Application.builder().token(BOT_TOKEN).read_timeout(10).write_timeout(10).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("registrar", registrar)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nombre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_edad)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_peso)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_altura)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_objetivo)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_metas)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_alergias)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("¡Hola! Usa /registrar para comenzar.")))
    app.add_handler(conv_handler)
    
    # Manejadores para el menú principal
    app.add_handler(MessageHandler(filters.Regex("🍽️ Recomendación de recetas"), recomendacion_recetas))
    app.add_handler(MessageHandler(filters.Regex("📊 Contar calorías del día"), contar_calorias))
    app.add_handler(MessageHandler(filters.Regex("🚪 Salir"), salir))
    app.add_handler(CallbackQueryHandler(manejar_alergias, pattern="^alergia_"))

    print("NutriBot en marcha 🚀")
    app.run_polling()

if __name__ == '__main__':
    main()
