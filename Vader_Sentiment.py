#!/usr/bin/python3

"""
    makes a sentiment analysis usning vader (valence aware dictionary and sentiment reasoner)
    
    @author mtzortzi
"""

import os
import csv
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


"""
VADER (Valence Aware Dictionary and sEntiment Reasoner): uses a lexicon and rule-based approach to evaluate the sentiment of text data. 
It's particularly well-suited for analyzing social media, news articles, and other forms of online text.

KEY FEATURES:
    Pre-Trained Sentiment Lexicon:
    VADER relies on a lexicon (a dictionary) of words that have been scored for their sentiment intensity (Positive words like "great," "awesome," or "fantastic" have high positive scores).
    Handles Sentiment Modifiers:
    VADER accounts for intensifiers, negations, and other modifiers that influence sentiment (Intensifiers: Words like "very" or "extremely" increase sentiment intensity). 
    Works Well for Short Text
    Emoticons, Slang, and Punctuation
    VADER recognizes emojis, internet slang, and punctuation to better capture sentiment in informal text ("I love it!! 😊" will have a stronger positive sentiment due to the exclamation points and smiley face).
    Scores for Sentiment Polarity:
    VADER provides a compound sentiment score and scores for each sentiment category:
        Positive Score: Measures the intensity of positive sentiment.
        Negative Score: Measures the intensity of negative sentiment.
        Neutral Score: Measures the intensity of neutral sentiment.
        Compound Score: A normalized score between -1 (most negative) and +1 (most positive). It reflects the overall sentiment of the text.
"""

path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/"

country =  'Greek'#'Spanish' #'Greek'#'Italian' #'Greek' #'Greek' #'Spanish'
newspaper = 'ladylike'#'elplural' #'documento' #'provocateur'#'ertnews'#'skai'#'popaganda'#'tanea'#'lifo'#'internazionale' #'openmigration'#'ansa' #'openpolis' #'il_giornale' #'il_fatto_quotidiano'#'kathimerini' #'athinorama'#'eldiario' #'proto_thema' #'eldiario' #'elpais'
text_df = pd.read_csv(path + country + '/' + 'all_articles_combined_' + newspaper +'.csv')

# Sentiment Analysis function
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    compound_score = sentiment_score['compound']

    if compound_score >= 0.05:
        return "Positive", compound_score
    elif compound_score <= -0.05:
        return "Negative", compound_score
    else:
        return "Neutral", compound_score
    
# Apply sentiment analysis to each row of the DataFrame
text_df['Sentiment'], text_df['Sentiment Score'] = zip(*text_df['Text'].apply(analyze_sentiment))

# Display the updated DataFrame
print(text_df[['Title', 'Text', 'Sentiment', 'Sentiment Score']])#, 'Final Classification']])

# Optionally save the result to a CSV file
output_path = path + country + '/' + 'sentiment_analysis_' + newspaper + '.csv'
text_df.to_csv(output_path, index=False)