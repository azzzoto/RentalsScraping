import bs4
import requests
from tqdm import tqdm
import pandas as pd

def next_page_immobiliare(num, url):
    """this function is needed to get the next page of the url we're scraping.
    It's customized for the immobiliare_scraper function

    Args:
        num (int): identifier of the page number we're looking at
        url (link): url of the page we're scraping 

    Returns:
        str: updated string with the new link at the new page
    """
    stringa = f"?pag={num}"
    return url + stringa

def price_formatter_immobiliare(str_price):
    str_price = (str_price.split("/")[0].split("€")[-1].strip())
    float_price =  "".join(str(str_price).split("."))
    return float(float_price)

def df_maker_immobiliare(url):

    ReadLink = requests.get(url)

    try:
        ReadLink.raise_for_status()
        SearchContent = bs4.BeautifulSoup(ReadLink.content, "html.parser")
        AllHouses = SearchContent.find(class_ = "nd-list in-realEstateResults")

        HouseNames = [item.text for item in AllHouses.find_all(class_ = "in-card__title")]
        HouseLinks = [item['href'] for item in AllHouses.find_all('a', href = True)]
        HousePrices = [item.text for item in AllHouses.find_all(class_ = "nd-list__item in-feat__item in-feat__item--main in-realEstateListCard__features--main")]

        constructor = []
        for name, link, price in (zip(HouseNames,HouseLinks,HousePrices)):
            constructor.append((name, price, link))
        data = pd.DataFrame.from_records(constructor, columns = ["Name", "Price (€)", 
                                                                "Link"])

        data["Price (€)"] = data["Price (€)"].apply(price_formatter_immobiliare)
        data["Data Annuncio"] = ["No_Data"]*data.shape[0]

        return data

    except requests.exceptions.HTTPError as err:
        print("\n-->DEBUG ERROR<--")
        print(err)

def immobiliare_flats(url_immobiliare, città):
    """returns results from scraper func

    Args:
        url_immobiliare (URL): url with the seach of the city
        citt (str): str of the city of the reasearch

    Returns:
        immobiliare_results: Pandas DataFrame with results
        n_immobiliare: total number of flats found.
    """
    df_to_concat = [df_maker_immobiliare(url_immobiliare)]
    for i in range(2,100):
        print(f"Scraping: run {i} from Immobiliare.it ...")
        df_temp = df_maker_immobiliare(next_page_immobiliare(i, url_immobiliare))
        df_to_concat.append(df_temp)
        if df_temp is None:
            #logs
            print("\n")
            print("-"*60)
            print("Avaiable pages ended: stopping...")
            print("-"*60)
            break
    immobiliare_results = pd.concat(df_to_concat)
    immobiliare_results["Città"] = [città]*immobiliare_results.shape[0]
    n_immobiliare = immobiliare_results.shape[0]

    return immobiliare_results, n_immobiliare