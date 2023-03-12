import bs4
import requests
from tqdm import tqdm
import pandas as pd

def next_page_immobiliare(num, url):
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