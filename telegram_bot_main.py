import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import pandas as pd

from updater import update_results
from src.utils import create_telegram_message, create_URLs
from src.subito.scraper import subito_flats
from src.immobiliare.scraper import immobiliare_flats

#bot settings - qui dovresti importarlo direttamente come file e non così zozzo
TOKEN = "6285394546:AAGn-Z-iwI-jY6RPguUdyBpt16JXGq-tByo"

#Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
) 

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text(
            'Ciao! Usa "/ImpostaRicerca <regione provincia città>" per cominciare ad utilizzare il bot!'
            )
    await update.message.reply_text(
        'Esempio: "/ImpostaRicerca sardegna cagliari cagliari"'
            )
    
async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Ricerca cancellata in modo corretto!" if job_removed else "Non hai nessuna ricerca settata."
    await update.message.reply_text(text)

async def set_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> list:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        #args is a list containing regione, provincia e città
        r, p, c = tuple(context.args)
        text = "Ricerca settata correttamente!"
        job_removed = remove_job_if_exists(str(chat_id), context)
    
        context.job_queue.run_once(
            searcher_appartamenti(r, p, c, chat_id), 
            when=0, 
            chat_id=chat_id, 
            name=str(chat_id)
            )
        
        if job_removed:
            text += "La ricerca precedente è stata eliminata."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Try again: '/ImpostaRicerca <regione provincia città>'")

    return [r, p, c, chat_id]

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

def searcher_appartamenti(regione, provincia, città, chat_id):
    url_immobiliare, url_subito = create_URLs(regione, provincia, città)

    #initial message creation 
    starting_text = f"""Creazione di una ricerca automatizzata per appartamenti
               --> regione {regione.capitalize()}, 
               --> provincia di {provincia.capitalize()}, 
               --> città di {città.capitalize()}"""

    #create starting message
    create_telegram_message(TOKEN, chat_id, starting_text)
    create_telegram_message(TOKEN, chat_id, "Starting flat search...")

    #----------------------------------------------immobiliare.it----------------------------------------------
    immobiliare_results, n_immobiliare = immobiliare_flats(url_immobiliare, città)
    #create message with first round of scraping
    create_telegram_message(TOKEN, chat_id, f"Numero di appartamenti trovati su Immobiliare.it: {n_immobiliare}")

    #------------------------------------------------subito.it--------------------------------------------------
    subito_results, n_subito = subito_flats(url_subito, città)
    #create message with first round of scraping
    create_telegram_message(TOKEN, chat_id, f"Numero di appartamenti trovati su Subito.it: {n_subito}")

    #---------------------------------------------FINAL RESULTS------------------------------------------------
    tot_apt = n_subito + n_immobiliare
    create_telegram_message(TOKEN, chat_id, f"Totale appartamenti trovati: {tot_apt}")
    final_results = pd.concat([subito_results, immobiliare_results])

    update_results(final_results, TOKEN, chat_id)

if __name__ == "__main__":
    main(TOKEN)