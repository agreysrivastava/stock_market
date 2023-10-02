from flask import Flask, request
from model.fetch_data import fetch_data
from model.train_data import train_data
app = Flask(__name__)


@app.route('/fetch_clients')
def hello_world():  # put application's code here
    return fetch_data.fetch_all_clients_data()

@app.route('/fetch_old_news')
def fetch_news():
    return fetch_data.save_news()

@app.route('/process_news')
def process_data():
    return train_data.process_news()

@app.route('/')
def home():
    return 'Page to be designed later'

if __name__ == '__main__':
    app.run(debug=True)
