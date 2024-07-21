import requests
from bs4 import BeautifulSoup
import pandas as pd

url_base = 'https://www.mojauto.rs'


def scrape_car(url):
    polja = ['Kubikaža', 'Snaga', 'Prešao kilometara', 'Proveri kilometražu', 'Tip motora', 'Pogon', 'Menjač', 'Broj brzina', 'Broj vrata', 'Broj sedišta', 'Strana volana', 'Klima', 'Boja', 'Boja unutrašnjosti', 'Kategorija']
    html = requests.get(url_base + url, timeout=5).text
    cur_soup = BeautifulSoup(html)
    price = cur_soup.find('span', {'class':'priceReal'}).text
    year = cur_soup.find('ul', {'class':'basicSingleData'}).find_all('li')[1].text.split(' ')[0]
    try:
        oprema = cur_soup.find(string='Oprema').findParent().find_next_sibling().find_all('li')
        oprema = [li.text for li in oprema]
    except:
        oprema = []
        print(url_base + url)
        print('oprema fucked')
    
    try:
        istorija = cur_soup.find(string='Poreklo i istorija vozila').findParent().findNextSibling().find_all('li')
        istorija = {item.find('span').text : item.find('strong').text for item in istorija}
    except:
        istorija = []
        print(url_base + url)
        print('istorija fucked')

    name = cur_soup.find('div', {'class':'singleTop'}).find('h1').text
    #print(name)

    cur = {}
    
    for i, li in enumerate(cur_soup.find('ul', {'class':'techSpec'}).find_all('li')):
        potential_field = polja[i]
        if potential_field in li.text:
            cur[potential_field] = li.text.replace(potential_field, "").strip()
        else:
            for j in range(i, len(polja)):
                if polja[j] in li.text:
                    cur[polja[j]] = li.text.replace(polja[j], "").strip()   
    
    cur['price'] = price
    cur['year'] = year
    cur['url'] = url_base + url
    cur['oprema'] = str(oprema)
    cur['istorija'] = str(istorija)
    cur['name'] = name 
    #cur['sold'] = False
    #print(cur)
    return cur

def scrape_page(url, df = None, updating = False):
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.text)

    kek = soup.find_all('a', {'class':'addTitle'})

    one_page = []
    for elem in kek:
        if updating:
            if (url_base + elem['href']) in df['url'].values: 
                #print('In')
                continue
        
        one_page.append(scrape_car(elem['href']))

    return one_page

if __name__ == "__main__":
    data = []
    for i in range(1,173):
        data += scrape_page(f'https://www.mojauto.rs/rezultat/status/automobili/poredjaj-po/oglas_najnoviji/po_stranici/20/prikazi_kao/lista/stranica/{i}'.format(i))
        print(str(i) + "/173")

    df = pd.DataFrame.from_dict(data)
    df.to_csv('kola_3.csv', index=False)