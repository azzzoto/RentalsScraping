import requests

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
