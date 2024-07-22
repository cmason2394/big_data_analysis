# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:00:59 2024

@author: cassi
"""
#import modules
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

#save csv file as pandas dataframe
df = pd.read_csv('C:/Users/cassi/OneDrive/Documents/School/CTU/Big_data_analytics/Tweets.csv')

'''
print(df.head())
print(df.columns)
print(df.text)
'''

# focus on tweet column in dataframe
tweets = df.text
#print(tweets)

# use tfidf to show important unigrams and bigrams for each tweet
vectorizer = TfidfVectorizer(ngram_range=(1,2))
weights = vectorizer.fit_transform(tweets)
#print(weights)

# Get the feature names (n-grams)
feature_names = vectorizer.get_feature_names_out()

'''
print (df_words.head())
print(weights.shape)
print(df_words.shape)
'''

# Function to get non-zero tfidf n-grams with their values, sorted by tfidf value
def get_nonzero_ngrams_with_values(vector, feature_names):
    non_zero_indices = vector.nonzero()[1] #for a row (tweet), get column names (ngrams) of nonzero tfidf values
    ngrams_with_tfidf = [(feature_names[idx], vector[0, idx]) for idx in non_zero_indices] # Create tuples of n-grams and their tfidf values
    ngrams_with_tfidf.sort(key=lambda x: x[1], reverse=True)  # Sort by TF-IDF value in descending order
    return ngrams_with_tfidf

# Apply the function to each row (tweet) of the sparse tfidf matrix to return a sorted list of relevant ngrams for each tweet
df['ngrams_with_tfidf'] = [get_nonzero_ngrams_with_values(weights[i], feature_names) for i in range(weights.shape[0])] #Use shape to find the number of rows through which to iterate
print(df[['airline_sentiment', 'negativereason', 'airline', 'text', 'ngrams_with_tfidf']].head(50))

# read dataframe to csv file
df.to_csv('airline_tweet_themes.csv')