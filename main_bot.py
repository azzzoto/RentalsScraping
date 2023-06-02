import numpy as np
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import requests

from telegram_utils import create_message
from subito_scraper import df_maker_subito, next_page_subito
from immobiliare_scraper import df_maker_immobiliare, next_page_immobiliare

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

#initial message creation 
starting_text = f"""Creazione di una ricerca automatizzata per appartamenti
           --> regione {regione.capitalize()}, 
           --> provincia di {provincia.capitalize()}, 
           --> città di {città.capitalize()}"""

#create starting message
create_message(TOKEN, chat_id, starting_text)
create_message(TOKEN, chat_id, "Starting flat search...")

df_to_concat = [df_maker_immobiliare(url_immobiliare)]
for i in range(2,100):
    print(f"Scraping: run {i} from Immobiliare.it ...")
    df_temp = df_maker_immobiliare(next_page_immobiliare(i, url_immobiliare))
    df_to_concat.append(df_temp)
    if df_temp is None:
        print("\n")
        print("-"*60)
        print("Avaiable pages ended: stopping...")
        print("-"*60)
        break
immobiliare_results = pd.concat(df_to_concat)
n_immobiliare = immobiliare_results.shape[0]

create_message(TOKEN, chat_id, f"Numero di appartamenti trovati su Immobiliare.it: {n_immobiliare}")

#print("Scraping: run 1 from Subito.it ...")
df_to_concat = [df_maker_subito(url_subito)]
for i in range(2,100):
    print(f"Scraping: run {i} from Subito.it ...")
    df_temp = df_maker_subito(next_page_subito(i, url_subito))
    df_to_concat.append(df_temp)
    if df_temp.shape[0] == 0:
        break
#print("\n")
#print("-"*60)
#print("Avaiable pages ended: stopping...")
#print("-"*60)
subito_results = pd.concat(df_to_concat)
n_subito = subito_results.shape[0]

create_message(TOKEN, chat_id, f"Numero di appartamenti trovati su Subito.it: {n_subito}")

tot_apt = n_subito + n_immobiliare

create_message(TOKEN, chat_id, f"Totale appartamenti trovati: {tot_apt}")

final_results = pd.concat([subito_results, immobiliare_results])

#leggo gli appartamenti trovati nel DB
historic_data = pd.read_excel("DB.xlsx", "Sheet1")
link_storico = historic_data.Link

#verifico se tra quelli nuovi trovati ce ne siano di mai visti nel DB
new_flats_links = list(set(final_results.Link)-set(link_storico))

if len(new_flats_links)>0:
    #se trovo link mai visti li seleziono dai risultati appena trovati
    new_records_to_add_to_DB = final_results.set_index("Link").loc[new_flats_links].reset_index()
    
    #mi creo un nuovo db combinato tra quelli vecchi e quelli nuovi
    new_data = pd.concat([historic_data, new_records_to_add_to_DB])

    #sovrascrivo il file
    new_data.to_excel("DB.xlsx")
    create_message(TOKEN, chat_id, f"Trovati {len(new_records_to_add_to_DB)} nuovi appartamenti")

    #mi scrivo i nuovi appartamenti
    for i in range(len(new_records_to_add_to_DB)):
        create_message(TOKEN, chat_id, new_records_to_add_to_DB.iloc[i,:])
else:
    create_message(TOKEN, chat_id, "Nessun nuovo appartamento trovato")