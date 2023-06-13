import logging
from telegram.ext import Application, CommandHandler
from bot import start, unset, set_search

#bot settings
with open("TOKEN.txt", "r") as f:
    TOKEN = f.read()

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
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("ImpostaRicerca", set_search))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main(TOKEN)