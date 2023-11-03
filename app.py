from flask import Flask, request, jsonify
from model.fetch_data import fetch_data
from model.train_data import train_data
from model.prediction_stock import prediction_stock
app = Flask(__name__)


@app.route('/fetch_clients')
def hello_world():  # put application's code here
    return fetch_data.fetch_all_clients_data()

@app.route('/fetch_old_news')
def fetch_news():
    return fetch_data.save_news()

@app.route('/process_news')
def process_data():
    print("API news called")
    return train_data.process_news()

@app.route('/preprocess_news_nlp')
def preprocess_news_nlp():
    print("Under api")
    return train_data.preprocess_news_for_nlp()

@app.route('/predict_stock', methods=['POST'])
def predict_stock():
    client = request.get_json().get('client')
    if not train_data.done_today():
        fetch_data.get_today_news()
        train_data.preprocess_news_for_nlp()
    result_map = prediction_stock.predict_each_price(client)
    return jsonify(result_map)

@app.route('/')
def home():
    print('Home')
    return 'Page to be designed later'

if __name__ == '__main__':
    app.run(debug=False)
