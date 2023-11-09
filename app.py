from flask import Flask, request, jsonify, render_template
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
    result_map = {}
    client = request.get_json().get('client')
    fetch_data.process_yesterday_news()
    fetch_data.get_today_news()
    train_data.preprocess_news_for_nlp()
    result_map['yesterday_map'] = prediction_stock.predict_each_price(client, True)
    result_map['today_map'] = prediction_stock.predict_each_price(client, False)
    result_map['today_prices'] = fetch_data.get_today_price(client)
    return jsonify(result_map)

@app.route('/today_price', methods=['POST'])
def today_price():
    client = request.get_json().get('client')
    fetch_data.get_today_price(client)
    return 'Done'
@app.route('/')
def home():
    print('Home')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
