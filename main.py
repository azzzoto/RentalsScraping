import numpy as np
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import requests

from src.telegram_utils import create_message
from src.subito.scraper import subito_flats
from src.immobiliare.scraper import immobiliare_flats
from updater import update_results

#bot settings
TOKEN = "6285394546:AAGn-Z-iwI-jY6RPguUdyBpt16JXGq-tByo"
chat_id = "223987710"

#flat research settings
regione = "sardegna"
provincia = "cagliari"
città = "cagliari"

url_immobiliare = f"https://www.immobiliare.it/affitto-case/{città}/"
url_subito = f"https://www.subito.it/annunci-{regione}/affitto/appartamenti/{provincia}/{città}/"
url_idealista = f"https://www.idealista.it/affitto-case/{provincia}-{città}/"

def main():
    #initial message creation 
    starting_text = f"""Creazione di una ricerca automatizzata per appartamenti
               --> regione {regione.capitalize()}, 
               --> provincia di {provincia.capitalize()}, 
               --> città di {città.capitalize()}"""

    #create starting message
    create_message(TOKEN, chat_id, starting_text)
    create_message(TOKEN, chat_id, "Starting flat search...")

    #----------------------------------------------immobiliare.it----------------------------------------------
    immobiliare_results, n_immobiliare = immobiliare_flats(url_immobiliare, città)
    #create message with first round of scraping
    create_message(TOKEN, chat_id, f"Numero di appartamenti trovati su Immobiliare.it: {n_immobiliare}")

    #------------------------------------------------subito.it--------------------------------------------------
    subito_results, n_subito = subito_flats(url_subito, città)
    #create message with first round of scraping
    create_message(TOKEN, chat_id, f"Numero di appartamenti trovati su Subito.it: {n_subito}")

    #----------------------------------------------idealista.it------------------------------------------------
    #TODO!

    #---------------------------------------------FINAL RESULTS------------------------------------------------
    tot_apt = n_subito + n_immobiliare
    create_message(TOKEN, chat_id, f"Totale appartamenti trovati: {tot_apt}")
    final_results = pd.concat([subito_results, immobiliare_results])

    update_results(final_results, TOKEN, chat_id)

if __name__ == "__main__":
    main()