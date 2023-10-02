import csv
from bs4 import BeautifulSoup
import requests
from flask import url_for
from datetime import datetime
import json
import random
from datetime import date, timedelta

class fetch_data:

    clients = {'4268801':'BAJAJFINSV',
               '3834113': 'POWERGRID',
               '81153': 'BAJFINANCE',
               '60417': 'ASIANPAINT',
               '633601': 'ONGC',
               '2714625': 'BHARTIARTL',
               '897537': 'TITAN',
               '232961': 'EICHERMOT',
               '1270529': 'ICICIBANK',
               '1510401': 'AXISBANK',
               '5582849': 'SBILIFE',
               '492033': 'KOTAKBANK',
               '4598529': 'NESTLEIND',
               '315393': 'GRASIM',
               '2953217': 'TCS',
               '134657': 'BPCL',
               '408065': 'INFY',
               '738561': 'RELIANCE',
               '119553': 'HDFCLIFE',
               '140033': 'BRITANNIA'
               }
    today = datetime.today().strftime('%Y-%m-%d')
    dates = ['2019-01-01_2019-12-31','2020-01-01_2020-12-31','2021-01-01_2021-12-31','2022-01-01_2022-12-31','2023-01-01_'+today]
    @staticmethod
    def data_fetch_from_zerodha(from_date, to_date, client):
        api_base = (f'https://kite.zerodha.com/oms/instruments/historical/{client}'
                    f'/day?user_id=ICG880&oi=1&from={from_date}&to={to_date}')
        headers = {
            'Accept': '* / *',
            'Accept - Encoding': 'gzip, deflate, br',
            'Accept - Language': 'en - US, en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
            'Authorization': 'enctoken Azr/pBG1RO8cQxugJsB4yBlMY21a5Vi7/fAqmsxY2sKNU7r2mMivk45aSl/tvGPRj2oLGYdwjZ5YXf0kGPRE95dEH7thsfrHX36+E3BK/YhDRhbDBX+iwg=='
        }

        response = requests.get(api_base, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def fetch_all_clients_data():
        for stock in fetch_data.clients:
            file_name = fetch_data.clients[stock]+'_5Y_data.csv'
            with open(url_for('static', filename = file_name),'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Entry Date", "Open price", "High Price", "Low Price", "Avg. price", "Volume"])
                for date in fetch_data.dates:
                    from_date = date.split('_')[0]
                    to_date = date.split('_')[1]
                    resp = fetch_data.data_fetch_from_zerodha(from_date, to_date, stock)
                    if resp != None:
                        for entry in resp['data']['candles']:
                            writer.writerow(entry[:-1])
        return 'Data fetched'

    @staticmethod
    def save_news():
        year = 2019
        mth = 1
        start = 43466
        start_date = date(2019, 1, 1)
        end_date = date.today()
        current_date = start_date
        file_name = 'News_Samples.tsv'
        with (open('C:/Users/agrey/PycharmProjects/stockPredictor/static/' + file_name, 'a+', newline='',encoding='utf-8') as file):
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["Entry Date","News Articles"])
            while current_date <= end_date:
                news_list = fetch_data.scrape_et_news(str(current_date.year), str(current_date.month), str(start))
                if news_list != None:
                    row = [current_date]
                    row.extend(news_list)
                    writer.writerow(row)
                current_date += timedelta(days=1)
                start = start+1
        file.close()
        return 'News Fetched'

    @staticmethod
    def scrape_et_news(year, mth, start):
        url = f'https://economictimes.indiatimes.com/archivelist/year-{year},month-{mth},starttime-{start}.cms'

        response = requests.get(url)
        news_list = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all('li')
            for item in items:
                if item.text == 'Most Read':
                    break
                news_list.append(item.text)

            news_list = random.sample(news_list, 40)
            # Print the extracted data
            return news_list

    @staticmethod
    def get_bing_news():
        subscription_key = "your subscription key"
        search_term = "Microsoft"
        search_url = "https://api.bing.microsoft.com/v7.0/news/search"
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = json.dumps(response.json())
        descriptions = [article["description"] for article in search_results["value"]]
        print(descriptions)

