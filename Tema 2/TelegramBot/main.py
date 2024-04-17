import logging
import re

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Expresión regular para detectar mensajes que contienen "Hola"
expresion_regular = re.compile(r"hello|hi|hey|hola", re.IGNORECASE)

#Expresiones de la práctica de vuelos (Hibrida)

patron_origen_destino_fecha = re.compile (r"volar de (\w+) a (\w+) el (\d{1,2} de \w+)", re.IGNORECASE)
patron_precio = re.compile (r"cuánto cuesta un vuelo de (\w+) a (\w+)", re.IGNORECASE) 
patron_ida_vuelta = re.compile (r"un vuelo de ida y vuelta de (\w+) a (\w+)", re.IGNORECASE)

#Otras expresiones añadidas :)

expresion_regular_numero_telefono = re.compile(r"(\d{3}[\s.-]\d{3}[\s.-]\d{4})", re.IGNORECASE)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message if it matches the regular expression."""
    message_text = update.message.text
    if expresion_regular.search(message_text):
        await update.message.reply_text("¡Hola! ¿Cómo estás?")
    elif resultado := patron_origen_destino_fecha.search(message_text):
        await update.message.reply_text(f"Buscar vuelo de {resultado.group(1)} a {resultado.group(2)} para el{resultado.group(3)}")
    elif resultado := patron_precio.search(message_text):
        await update.message.reply_text(f"Consultar precio de vuelo de {resultado.group(1)} a {resultado.group(2)}")
    elif resultado := patron_ida_vuelta.search(message_text):
        await update.message.reply_text(f"Buscar vuelo de ida y vuelta de {resultado.group(1)} a {resultado.group(2)}")
    elif resultado := expresion_regular_numero_telefono.search(message_text): 
        await update.message.reply_text(f"Número de teléfono encontrado: {resultado.group(1)} ")   
    else:
        await update.message.reply_text("No entendí tu mensaje.")



def main() -> None:
    """Start the bot."""
    application = Application.builder().token("6780118627:AAHkgEkFOhG9IJD2Y5PPC1i9Ss-kgpNNxn4").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()