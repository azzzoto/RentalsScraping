import pandas as pd
from src.utils import create_telegram_message

def update_results(final_results, TOKEN, chat_id):
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
        new_data.to_excel("DB.xlsx", index = False)
        create_telegram_message(TOKEN, chat_id, f"Trovati {len(new_records_to_add_to_DB)} nuovi appartamenti")

        #mi scrivo i nuovi appartamenti
        for annuncio in new_records_to_add_to_DB.values:
            create_telegram_message(TOKEN, chat_id, annuncio)
    else:
        create_telegram_message(TOKEN, chat_id, "Nessun nuovo appartamento trovato")