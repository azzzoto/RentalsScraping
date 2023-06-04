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

            #TODO 
            # qui ho momentaneamente commentato il codice per evitare che lo scraper dovesse
            # fare "inner-scraping" all'interno dello stesso annuncio per andare più veloce 
            # ma sarebbe da sistemare l'aggiunta di altri dettagli tra cui la data di inserimento

            #descrizione = requests.get(link)
            #zuppa = bs4.BeautifulSoup(descrizione.text, "html.parser")
            ##text_descr = zuppa.find(class_ = "grid_detail-component__7sBtj grid_description__rEv3i")
            ##annuncio_txt_descr = text_descr.find('p').contents[0]

            ##qui data
            #data_aggiunta = zuppa.find(class_ = "index-module_sbt-text-atom__ed5J9 index-module_token-caption__TaQWv size-normal index-module_weight-book__WdOfA index-module_insertion-date__MU4AZ")
            #data_annuncio = data_aggiunta.text

            #temporary, see comment above
            data_annuncio = "No_Data"

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

def subito_flats(url_subito, città):
    """returns results from the scraping of subito.it website

    Args:
        url_subito (url): url construction of the query
        città (__str__): str with the city we're looking for

    Returns:
        subito_results: DataFrame containing the results of the query for flats
        n_subito: returns the number of flats found (subito_results.shape[0])
    """

    print("Scraping: run 1 from Subito.it ...")
    df_to_concat = [df_maker_subito(url_subito)]
    for i in range(2,100):
        print(f"Scraping: run {i} from Subito.it ...")
        df_temp = df_maker_subito(next_page_subito(i, url_subito))
        df_to_concat.append(df_temp)
        if df_temp.shape[0] == 0:
            break
    print("\n")
    print("-"*60)
    print("Avaiable pages ended: stopping...")
    print("-"*60)
    subito_results = pd.concat(df_to_concat)
    subito_results["Città"] = [città]*subito_results.shape[0]
    n_subito = subito_results.shape[0]

    return subito_results, n_subito