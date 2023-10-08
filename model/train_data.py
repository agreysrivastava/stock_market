import spacy
import csv
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
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
        doc = train_data.nlp(text)
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
    def create_wordclouds(lda_model, vectorizer):
        for i, topic_weights in enumerate(lda_model.components_):
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(
                dict(zip(vectorizer.get_feature_names_out(), topic_weights)))
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.title(f"Topic {i + 1} Word Cloud")
            plt.show()

    @staticmethod
    def preprocess_news_for_nlp():
        df = pd.read_csv(os.getcwd()+'/static/Processed_News.tsv', delimiter='\t')
        for count in range(1,40):
            try:
                df["News Articles"+str(count)] = df["News Articles"+str(count)].apply(train_data.preprocess_text)
                tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=2, stop_words="english")
                tfidf_matrix = tfidf_vectorizer.fit_transform(df["News Articles"+str(count)])
                # Topic Modeling (LDA)
                lda = LatentDirichletAllocation(n_components=5, random_state=42)
                lda.fit(tfidf_matrix)
                df["topic"+str(count)] = lda.transform(tfidf_matrix).argmax(axis=1)

                top_words = train_data.get_top_words(lda, tfidf_vectorizer)
                for i, words in enumerate(top_words):
                    print(f"Topic {i + 1}: {', '.join(words)}")
                train_data.create_wordclouds(lda, tfidf_vectorizer)
            except :
                print()
        return 'Done'
