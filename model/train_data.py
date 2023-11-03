import spacy
import csv
import pandas as pd
from datetime import date
from sklearn.feature_extraction.text import TfidfVectorizer
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
                                    line = line.replace(yesterday, today.strftime('%Y-%m-%d'),1)
                                    writer.writerow(line.split('\t'))
                                    date_list.append(yesterday)
                                    break
                    return date_list

    nlp = spacy.load("en_core_web_sm")
    @staticmethod
    def preprocess_text(text):
        doc = train_data.nlp(str(text))
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        return " ".join(tokens)

    @staticmethod
    def get_top_words(lda_model, vectorizer, n_words=10):
        top_words = []
        for topic_weights in lda_model.components_:
            top_word_indices = topic_weights.argsort()[-n_words:][::-1]
            top_words.append([vectorizer.get_feature_names_out()[i] for i in top_word_indices])
        return top_words

    @staticmethod
    def merge_columns(row):
        news_text = ""
        for count in range(1, len(row)):
            news_text += ("  "+ str(row["News Articles" + str(count)]))
        return f"{news_text}"

    @staticmethod
    def done_today():
        df = pd.read_csv(os.getcwd()+'/static/Final_Dataframe.csv')
        last_date = df['Entry Date'].iloc[-1]
        if last_date == str(date.today()):
            print(True)
            return True
        return False

    @staticmethod
    def preprocess_news_for_nlp():
        df = pd.read_csv(os.getcwd()+'/static/Processed_News.tsv', delimiter='\t')
        df.dropna()
        df["News Articles"] = df.apply(train_data.merge_columns, axis=1)
        df["News Articles"] = df["News Articles"].apply(train_data.preprocess_text)
        tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=2, stop_words="english", max_features=1600)
        tfidf_matrix = tfidf_vectorizer.fit_transform(df["News Articles"])
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
        print(tfidf_df.iloc[0:10, :])
        print(tfidf_df.shape, '  =======================  ')
        tfidf_df['Entry Date'] = df['Entry Date']
        tfidf_df.to_csv(os.getcwd()+'/static/Final_Dataframe.csv', index=False)
        return 'Done'
