import bs4
import requests
from tqdm import tqdm
import pandas as pd

def next_page_idealista(num, url):
  stringa = f"/lista-{num}.htm"
  return url + stringa

"""
from bs4 import BeautifulSoup
from selenium import webdriver

PATH = 'C:\Program Files (x86)\chromedriver.exe'


l=list()
o={}

target_url = "https://www.idealista.it/en/affitto-case/cagliari-cagliari/"


driver=webdriver.Chrome(PATH)
driver.get(target_url)

resp = driver.page_source
#driver.close()
SearchContent = bs4.BeautifulSoup(resp.content, "html.parser")

print(SearchContent, type(SearchContent))
"""