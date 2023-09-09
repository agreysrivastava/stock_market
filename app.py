from flask import Flask
from model.fetch_data import fetch_data

app = Flask(__name__)


@app.route('/fetch_clients')
def hello_world():  # put application's code here
    return fetch_data.fetch_all_clients_data()

@app.route('/fetch_news')
def fetch_news():
    return fetch_data.fetch_news_api()

@app.route('/')
def home():
    return 'Page to be designed later'

if __name__ == '__main__':
    app.run(debug=True)
