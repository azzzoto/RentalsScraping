import bs4
import requests
from tqdm import tqdm
import pandas as pd

def next_page_subito(num, url):
  stringa = f"?o={num}"
  return url + stringa

def df_maker_subito(url):

    page_subito = requests.get(url)

    try:
        page_subito.raise_for_status()
        soup = bs4.BeautifulSoup(page_subito.text, "html.parser")
        products_list = soup.find(class_ = "ListingContainer_container__4DQ56 container")
        products_list_items_annunci = products_list.find_all(class_ = "items__item item-card item-card--big BigCard-module_card__Exzqv")

        constructor = []

        for product in (products_list_items_annunci):
            link = product.find('a', href = True)['href']
            price = product.find('p')
            name = product.find('h2')

            descrizione = requests.get(link)
            zuppa = bs4.BeautifulSoup(descrizione.text, "html.parser")
            #text_descr = zuppa.find(class_ = "grid_detail-component__7sBtj grid_description__rEv3i")
            #annuncio_txt_descr = text_descr.find('p').contents[0]

            #qui data
            data_aggiunta = zuppa.find(class_ = "index-module_sbt-text-atom__ed5J9 index-module_token-caption__TaQWv size-normal index-module_weight-book__WdOfA index-module_insertion-date__MU4AZ")
            data_annuncio = data_aggiunta.text

            if len(price) > 0:
                constructor.append((name.contents[0], price.contents[0], link, data_annuncio))
            else:
                constructor.append((name.contents[0], "0 €", link, data_annuncio))

        final_df =  pd.DataFrame.from_records(constructor, 
                                              columns = ["Name", "Price (€)", 
                                                        "Link", "Data Annuncio"]
                                             )

        final_df["Price (€)"] = final_df["Price (€)"].apply(lambda x: (str(x).split("€")[0]).strip())
        final_df["Price (€)"] = final_df["Price (€)"].apply(lambda x: "".join(str(x).split(".")))
        #final_df["Price (€)"] = final_df["Price (€)"].apply(lambda x: float(x))

        return final_df.sort_values(by = "Price (€)").reset_index().iloc[:,1:]
        
    except requests.exceptions.HTTPError as err:
        print("\n-->DEBUG ERROR<--")
        print(err)

