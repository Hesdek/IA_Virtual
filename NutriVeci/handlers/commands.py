from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

# Estados de la conversación
NOMBRE, EDAD, PESO, ALTURA, OBJETIVO, METAS, ALERGIAS = range(7)

user_data_temp = {}

async def registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Vamos a comenzar tu registro. ¿Cuál es tu nombre? 📝")
    return NOMBRE

async def recibir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id] = {"nombre": update.message.text}
    await update.message.reply_text("📅 ¿Cuántos años tienes?")
    return EDAD

async def recibir_edad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id]["edad"] = int(update.message.text)
    await update.message.reply_text("⚖️ ¿Cuál es tu peso en kg? (Ejemplo: 70.5)")
    return PESO

async def recibir_peso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id]["peso"] = float(update.message.text)
    await update.message.reply_text("📏 ¿Cuál es tu altura en cm? (Ejemplo: 170)")
    return ALTURA

async def recibir_altura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id]["altura"] = float(update.message.text)
    
    # Crear un teclado con opciones
    keyboard = [["🏋️ Ganar peso", "⚡ Perder peso"], ["⚖️ Mantener peso"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "🎯 ¿Cuál es tu objetivo principal? Selecciona una opción:",
        reply_markup=reply_markup
    )
    return OBJETIVO

async def recibir_objetivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id]["objetivo"] = update.message.text
    
    # Crear un teclado con opciones para metas adicionales
    keyboard = [
        ["⚡ Aumentar energía diaria", "🍎 Contribuir a hábitos saludables"],
        ["💰 Ahorrar en costos de comida", "😌 Reducir estrés"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "✨ ¿Tienes alguna meta adicional? Selecciona una opción:",
        reply_markup=reply_markup
    )
    return METAS

async def recibir_metas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id]["metas"] = update.message.text
    
    # Crear un teclado con opciones para alergias
    keyboard = [
        ["🌾 Gluten", "🥜 Maní", "🍳 Huevo"],
        ["🥛 Lactosa", "🐟 Pescado", "🍤 Mariscos"],
        ["❌ Ninguna"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "🤔 ¿Tienes alguna alergia alimentaria? Selecciona una opción:",
        reply_markup=reply_markup
    )
    return ALERGIAS

async def recibir_alergias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id]["alergias"] = update.message.text
    data = user_data_temp.pop(update.effective_chat.id)
    
    # Resumen final
    await update.message.reply_text(
        "✅ ¡Registro completo! 🎉\n"
        f"Gracias, {data['nombre']} 🙌. Aquí está un resumen de tus datos:\n\n"
        f"📅 Edad: {data['edad']} años\n"
        f"⚖️ Peso: {data['peso']} kg\n"
        f"📏 Altura: {data['altura']} cm\n"
        f"🎯 Objetivo: {data['objetivo']}\n"
        f"✨ Metas adicionales: {data['metas']}\n"
        f"⚠️ Alergias: {data['alergias']}\n\n"
        "¡Espero poder ayudarte a alcanzar tus metas! 💪"
    )
    
    # Mostrar el menú principal
    keyboard = [
        ["🍽️ Recomendación de recetas", "📊 Contar calorías del día"],
        ["🚪 Salir"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "📋 Menú principal:\n"
        "Selecciona una opción para continuar:",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp.pop(update.effective_chat.id, None)
    await update.message.reply_text("❌ Registro cancelado. Si necesitas ayuda, no dudes en intentarlo de nuevo. 😊")
    return ConversationHandler.END

async def recomendacion_recetas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍽️ Aquí tienes una receta recomendada para ti:\n"
        "- Ensalada de quinoa con aguacate 🥗\n"
        "- Pollo a la parrilla con vegetales 🐓🥦\n"
        "- Smoothie de frutas 🍓🍌\n\n"
        "¡Espero que te guste! 😋"
    )

async def contar_calorias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Para contar tus calorías del día, ingresa los alimentos que has consumido.\n"
        "Por ejemplo: '2 manzanas, 1 taza de arroz, 150g de pollo'."
    )

async def salir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚪 ¡Gracias por usar NutriBot! Si necesitas algo más, no dudes en escribirme. 😊"
    )
