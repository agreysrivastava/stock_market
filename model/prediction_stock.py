import os
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from datetime import datetime, date, timedelta

class prediction_stock:

    @staticmethod
    def process_date_values(text):
        return text.split('T')[0]
    @staticmethod
    def load_X_Y(client, slice, search_date):
        X_df = pd.read_csv(os.getcwd()+'/static/Final_Dataframe.csv')
        idx = -1
        for i in range(1170,len(X_df)):
            if X_df['Entry Date'][i] == search_date:
                idx = i
        Y_df = pd.read_csv(os.getcwd()+f'/static/{client}_5Y_data.csv')
        Y_df['Entry Date'] = Y_df['Entry Date'].apply(prediction_stock.process_date_values)
        merged_df = pd.merge(X_df, Y_df, on='Entry Date', how='inner') #will use if required
        if slice == -1:
            return merged_df.iloc[:,:-6], merged_df.iloc[:,slice:], X_df.iloc[-1,:-1]
        return merged_df.iloc[:,:-6], merged_df.iloc[:,slice:slice+1], X_df.iloc[idx,:-1] #use -5 open, -4 High, -3 Low, -2 avg

    @staticmethod
    def predict_each_price(client, is_yesterday):
        response_map = {}
        search_date = datetime.now()
        if is_yesterday:
            search_date = search_date - timedelta(days=1)
        search_date = search_date.strftime('%Y-%m-%d')
        X, Y, sample = prediction_stock.load_X_Y(client, -5, search_date)
        pred_open, acc_open = prediction_stock.predict_stock_attribute(X, Y, sample)
        X, Y, sample = prediction_stock.load_X_Y(client, -4, search_date)
        pred_high, acc_high = prediction_stock.predict_stock_attribute(X, Y, sample)
        X, Y, sample = prediction_stock.load_X_Y(client, -3, search_date)
        pred_low, acc_low = prediction_stock.predict_stock_attribute(X, Y, sample)
        X, Y, sample = prediction_stock.load_X_Y(client, -2, search_date)
        pred_avg, acc_avg = prediction_stock.predict_stock_attribute(X, Y, sample)
        X, Y, sample = prediction_stock.load_X_Y(client, -1, search_date)
        pred_vol, acc_vol = prediction_stock.predict_stock_attribute(X, Y, sample)
        avg_acc = (acc_avg+ acc_low+ acc_high+ acc_open)/4
        response_map['open'] = pred_open
        response_map['high'] = pred_high
        response_map['low'] = pred_low
        response_map['avg'] = pred_avg
        response_map['volume'] = pred_vol
        response_map['avg_accuracy'] = round(abs(avg_acc)*100, 2)
        print(response_map)
        return response_map

    @staticmethod
    def predict_stock_attribute(X, Y, sample):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
        regressor = SVR(kernel='rbf')
        regressor.fit(X_train, Y_train)
        y_pred = regressor.predict(X_test)
        r2 = r2_score(Y_test, y_pred)
        predicted_result = regressor.predict(sample.values.reshape(1, 1600))[0]
        return predicted_result, r2

