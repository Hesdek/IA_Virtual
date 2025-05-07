from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
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
    user_data_temp[update.effective_chat.id]["altura"] = float(update.message.text) / 100  # Convertir a metros
    
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
        [InlineKeyboardButton("🌾 Gluten", callback_data="alergia_gluten")],
        [InlineKeyboardButton("🥜 Maní", callback_data="alergia_mani")],
        [InlineKeyboardButton("🍳 Huevo", callback_data="alergia_huevo")],
        [InlineKeyboardButton("🥛 Lactosa", callback_data="alergia_lactosa")],
        [InlineKeyboardButton("🐟 Pescado", callback_data="alergia_pescado")],
        [InlineKeyboardButton("🍤 Mariscos", callback_data="alergia_mariscos")],
        [InlineKeyboardButton("❌ Ninguna", callback_data="alergia_ninguna")],
        [InlineKeyboardButton("✅ Listo", callback_data="alergia_listo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤔 ¿Tienes alguna alergia alimentaria? Selecciona una o varias opciones y presiona '✅ Listo' cuando termines:",
        reply_markup=reply_markup
    )
    return ALERGIAS

async def manejar_alergias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Obtener la alergia seleccionada
    alergia = query.data.replace("alergia_", "")
    
    # Inicializar la lista de alergias si no existe
    if "alergias" not in user_data_temp[query.message.chat_id]:
        user_data_temp[query.message.chat_id]["alergias"] = []
    
    # Si el usuario presiona "Listo", pasa al resumen final
    if alergia == "listo":
        alergias = ", ".join(user_data_temp[query.message.chat_id]["alergias"])
        if not alergias:
            alergias = "Ninguna"
        await query.edit_message_text(
            f"⚠️ Has seleccionado las siguientes alergias: {alergias}"
        )
        return await mostrar_resumen(query.message.chat_id, context)
    
    # Si selecciona "Ninguna", limpia las alergias y pasa al resumen
    if alergia == "ninguna":
        user_data_temp[query.message.chat_id]["alergias"] = ["Ninguna"]
        await query.edit_message_text("⚠️ No tienes alergias alimentarias.")
        return await mostrar_resumen(query.message.chat_id, context)
    
    # Agregar o quitar la alergia seleccionada
    if alergia in user_data_temp[query.message.chat_id]["alergias"]:
        user_data_temp[query.message.chat_id]["alergias"].remove(alergia)
    else:
        user_data_temp[query.message.chat_id]["alergias"].append(alergia)
    
    # Actualizar el mensaje con las alergias seleccionadas
    alergias = ", ".join(user_data_temp[query.message.chat_id]["alergias"])
    await query.edit_message_text(
        f"🤔 ¿Tienes alguna alergia alimentaria? Selecciona una o varias opciones y presiona '✅ Listo' cuando termines:\n\n"
        f"Seleccionadas: {alergias}"
    )

async def mostrar_resumen(chat_id, context):
    data = user_data_temp.pop(chat_id)
    
    # Calcular el IMC
    imc = data["peso"] / (data["altura"] ** 2)
    if imc < 18.5:
        clasificacion_imc = "Bajo peso"
    elif 18.5 <= imc < 24.9:
        clasificacion_imc = "Peso normal"
    elif 25 <= imc < 29.9:
        clasificacion_imc = "Sobrepeso"
    else:
        clasificacion_imc = "Obesidad"
    
    # Resumen final
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "✅ ¡Registro completo! 🎉\n"
            f"Gracias, {data['nombre']} 🙌. Aquí está un resumen de tus datos:\n\n"
            f"📅 Edad: {data['edad']} años\n"
            f"⚖️ Peso: {data['peso']} kg\n"
            f"📏 Altura: {data['altura'] * 100:.1f} cm\n"
            f"🎯 Objetivo: {data['objetivo']}\n"
            f"✨ Metas adicionales: {data['metas']}\n"
            f"⚠️ Alergias: {', '.join(data['alergias'])}\n\n"
            f"📊 Tu IMC es: {imc:.1f} ({clasificacion_imc})\n\n"
            "¡Espero poder ayudarte a alcanzar tus metas! 💪"
        )
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
