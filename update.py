import requests
from bs4 import BeautifulSoup
import pandas as pd
from scraping import scrape_page

df = pd.read_csv('kola.csv')
for i in range(1,173):
    to_be_added = scrape_page(f'https://www.mojauto.rs/rezultat/status/automobili/poredjaj-po/oglas_najnoviji/po_stranici/20/prikazi_kao/lista/stranica/{i}'.format(i), df=df, updating=True)
    if len(to_be_added) > 0:
        pd.DataFrame.from_dict(to_be_added).to_csv('kola_3.csv',mode='a', header=False, index=False)
    print(str(i) + "/173")