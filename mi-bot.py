# mi-bot.py
import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Configuración básica de log y variables de entorno
# --------------------------------------------------------------------------
# Es una buena práctica para rastrear errores
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Lee el token de la variable de entorno
# CRÍTICO: Si la variable no está, el programa termina aquí.
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("FATAL: La variable de entorno 'TELEGRAM_BOT_TOKEN' no está configurada.")
    exit()

# 2. Funciones de consumo de API (Nuestro Backend)
# --------------------------------------------------------------------------
# API gratuita para hechos curiosos:
API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"

def obtener_dato_curioso():
    """Consume la API y devuelve un dato curioso."""
    try:
        response = requests.get(API_URL)
        # Lanza una excepción para errores 4xx/5xx
        response.raise_for_status() 
        data = response.json()
        
        # El dato viene en el campo 'text' de la respuesta JSON
        return data.get('text', 'No se pudo obtener el dato curioso.')
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al consumir la API: {e}")
        return "Lo siento, tengo problemas para conectarme con la API."


# 3. Manejadores de Telegram (Nuestra Interfaz/Frontend)
# --------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /start."""
    await update.message.reply_text(f'¡Hola! Soy tu Minibot. Usa /dato para obtener un dato curioso.')

async def dato(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /dato consumiendo la API."""
    
    # 🧠 Llama a nuestra función de Backend (consumo de API)
    dato = obtener_dato_curioso()
    
    # 🗣️ Envía el resultado al usuario
    await update.message.reply_text(dato)


# 4. Función Principal
# --------------------------------------------------------------------------
def main() -> None:
    """Inicia el bot."""
    # Crea la aplicación y le pasa el token del bot.
    application = Application.builder().token(BOT_TOKEN).build()

    # Registra los comandos (Handlers)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dato", dato))

    # Inicia el bot (polling: escucha nuevos mensajes)
    logging.info("El Bot está en línea y escuchando...")
    application.run_polling(poll_interval=1)

if __name__ == '__main__':
    main()