import requests
import pandas as pd
import os

from src.immobiliare.scraper import immobiliare_flats
from src.subito.scraper import subito_flats

def create_telegram_message(TOKEN, chat_id, text):
    """given a token, and a chat_id, creates a message with text

    Args:
        TOKEN (str): token for telegram bot by botfather
        chat_id (str): id chat of the bot
        text (str): text that has to be sent
    """
    url_bot = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
    return requests.get(url_bot).json()

def create_URLs(regione, provincia, città):
    """this function creates the URLs to scrape apartments for 
       a) immobiliare.it
       b) subito.it
       c) idealista.it

    Args:
        regione (_str_): name of the italian region in which we're looking for a flat
        provincia (_str_): name of the italian province in which we're looking for a flat
        città (_str_): name of the italian city in which we're looking for a flat
    """

    #secondo me qui poi bisogna fare anche 
    #---> assert regione in lista_regioni and so on...

    assert type(regione) == str
    assert type(provincia) == str
    assert type(città) == str

    regione = regione.lower()
    provincia = provincia.lower()
    città = città.lower()

    url_immobiliare = f"https://www.immobiliare.it/affitto-case/{città}/"
    url_subito = f"https://www.subito.it/annunci-{regione}/affitto/appartamenti/{provincia}/{città}/"
    #url_idealista = f"https://www.idealista.it/affitto-case/{provincia}-{città}/"

    return url_immobiliare, url_subito#, url_idealista

def update_results(final_results, TOKEN, chat_id):
    #leggo gli appartamenti trovati nel DB

    if os.path.isfile(f"DB_{chat_id}.xlsx"):
        historic_data = pd.read_excel(f"DB_{chat_id}.xlsx", "Sheet1")
        link_storico = historic_data.Link
    else:
        historic_data = pd.DataFrame(columns=["Name", "Price (€)", "Link", "Data Annuncio", "Città"])
        link_storico = []

    #verifico se tra quelli nuovi trovati ce ne siano di mai visti nel DB
    new_flats_links = list(set(final_results.Link)-set(link_storico))

    if len(new_flats_links)>0:
        #se trovo link mai visti li seleziono dai risultati appena trovati
        new_records_to_add_to_DB = final_results.set_index("Link").loc[new_flats_links].reset_index()

        #mi creo un nuovo db combinato tra quelli vecchi e quelli nuovi
        new_data = pd.concat([historic_data, new_records_to_add_to_DB])

        #sovrascrivo il file
        new_data.to_excel(f"DB_{chat_id}.xlsx", index = False)
        create_telegram_message(TOKEN, chat_id, f"Trovati {len(new_records_to_add_to_DB)} nuovi appartamenti")

        #mi scrivo i nuovi appartamenti
        for annuncio in new_records_to_add_to_DB.values:
            create_telegram_message(TOKEN, chat_id, annuncio)
    else:
        create_telegram_message(TOKEN, chat_id, "Nessun nuovo appartamento trovato")

def searcher_appartamenti(regione, provincia, città, TOKEN, chat_id):
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
