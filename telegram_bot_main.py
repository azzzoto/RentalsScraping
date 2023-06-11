import logging
import pandas as pd
from telegram.ext import Application, CommandHandler
from bot import start, unset, set_search

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