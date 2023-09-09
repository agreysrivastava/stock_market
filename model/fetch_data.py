import csv

import requests
from flask import url_for
from datetime import datetime

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
            'Authorization': 'enctoken VIjO2tw7waRLIaZZOyop+8SwaXZkrJvYPNPka301on5LmvWrhJJ06ypq/tb9Kum8HWRv9zEXcGl7nMjxfB7jgz/kL2Ykhrru7jwhr+BHCNhlWmmwcWsiTw=='
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
            with open('C:/Users/agrey/PycharmProjects/stockPredictor/static/'+file_name,'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Entry Date", "Open price", "High Price", "Low Price"])
                for date in fetch_data.dates:
                    from_date = date.split('_')[0]
                    to_date = date.split('_')[1]
                    resp = fetch_data.data_fetch_from_zerodha(from_date, to_date, stock)
                    if resp != None:
                        for entry in resp['data']['candles']:
                            writer.writerow(entry[:-3])
        return 'Data fetched'

    @staticmethod
    def fetch_news_api():
        api_key = '5e739d4ac4fd4eb195a078470613bd77'

        endpoint = 'https://newsapi.org/v2/everything'
        params = {
            'apiKey': api_key,
            'q': 'your_keyword',  # Replace with your search keyword
            'from': '2023-07-01',  # Replace with your start date
            'to': '2023-07-31',  # Replace with your end date
        }

        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            articles = data['articles']

            for article in articles:
                print(f"Title: {article['title']}")
                print(f"Source: {article['source']['name']}")
                print(f"Published At: {article['publishedAt']}")
                print(f"Description: {article['description']}\n")
        else:
            print(f"Error: {response.status_code}")

