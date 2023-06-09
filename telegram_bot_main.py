import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
#logging.basicConfig(
#    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
#) 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text(
            f"Ciao! Usa /ImpostaRicerca per cominciare ad utilizzare il bot!"
            )
            

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def set_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> list:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        print("------------------",context.args)
        # args[0] should contain the time for the timer in seconds
        r, p, c = tuple(context.args)
        print("<-------------<", r, p, c)

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(r, p, c, chat_id=chat_id, name=str(chat_id))

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /ImpostaRicerca <regione provincia città>")

    return [r, p, c, chat_id]

def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6285394546:AAGn-Z-iwI-jY6RPguUdyBpt16JXGq-tByo").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("ImpostaRicerca", set_search))
    #application.add_handler(CommandHandler("unset", unset))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()