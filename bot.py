from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from utils import searcher_appartamenti

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
    with open("TOKEN.txt", "r") as f:
        TOKEN = f.read()
        
    chat_id = update.effective_message.chat_id
    try:
        #args is a list containing regione, provincia e città
        r, p, c = tuple(context.args)
        text = "Ricerca settata correttamente!"
        job_removed = remove_job_if_exists(str(chat_id), context)
        await update.effective_message.reply_text(text)
    
        context.job_queue.run_once(
            searcher_appartamenti(r, p, c, TOKEN, chat_id), 
            when=0, 
            chat_id=chat_id, 
            name=str(chat_id)
            )
        
        if job_removed:
            text += "La ricerca precedente è stata eliminata."
        
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Try again: '/ImpostaRicerca <regione provincia città>'")

    return [r, p, c, chat_id]