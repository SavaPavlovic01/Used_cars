import pandas as pd
import requests
import datetime

url_base = 'https://www.mojauto.rs'

def check_if_sold(df:pd.DataFrame, df_sold:pd.DataFrame):
    cnt = 0
    sold = []
    size = len(df)
    for i, url in enumerate(df['url']):
        response = requests.get(url, timeout=5)
        #if url in df_sold['url'].values: continue
        if response.status_code != 200:
            cnt += 1
            sold.append(url)
        print(str(i + 1) + "/" + str(size))
    print(sold)
    sold_df = df[df['url'].isin(sold)]
    sold_df['date'] = datetime.datetime.today()
    sold_df.to_csv('prodata_kola.csv',mode='a', index=False, header=False)

df_sold = pd.read_csv('prodata_kola.csv')
df = pd.read_csv('kola_3.csv')
check_if_sold(df, df_sold)