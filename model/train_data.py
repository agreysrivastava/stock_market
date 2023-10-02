import requests
import csv
from flask import url_for
from model.fetch_data import fetch_data
from datetime import datetime, timedelta
import os

class train_data:
    client_list = fetch_data.clients.values()
    @staticmethod
    def process_news():
        print("Current Working Directory:", os.getcwd())
        date_list = []
        with open(os.getcwd()+'/static/News_Samples.tsv','r+',newline='',encoding='utf-8') as newsfile:
            with open(os.getcwd()+'/static/TCS_5Y_data.csv','r+',newline='') as stockfile:
                with open(os.getcwd()+'/static/Processed_News.tsv','w+',newline='',encoding='utf-8') as outputfile:
                    writer = csv.writer(outputfile, delimiter='\t')
                    writer.writerow(["Entry Date","News Articles"])
                    for entry in stockfile:
                        date = entry.split(',')[0].split('T')[0]
                        if date != '2019-01-01' and date != 'Entry Date':
                            today = datetime.strptime(date, '%Y-%m-%d')
                            yesterday = today - timedelta(days=1)
                            yesterday = yesterday.strftime('%Y-%m-%d')
                            for line in newsfile:
                                line = line.split('\r')[0]
                                if line.split('\t')[0] == yesterday:
                                    writer.writerow(line.split('\t'))
                                    date_list.append(yesterday)
                                    break
                    return date_list