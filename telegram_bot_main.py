import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import pandas as pd

from updater import update_results
from bot import remove_job_if_exists, start, unset, set_search
from src.utils import create_telegram_message, create_URLs
from src.subito.scraper import subito_flats
from src.immobiliare.scraper import immobiliare_flats

#bot settings - qui dovresti importarlo direttamente come file e non così zozzo
TOKEN = "6285394546:AAGn-Z-iwI-jY6RPguUdyBpt16JXGq-tByo"

#Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
) 

def main(TOKEN) -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("ImpostaRicerca", set_search))
    application.add_handler(CommandHandler("unset", unset))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main(TOKEN)