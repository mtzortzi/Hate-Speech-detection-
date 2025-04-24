#!/usr/bin/python3

"""
    makes a sentiment analysis usning vader (valence aware dictionary and sentiment reasoner)
    
    @author mtzortzi
"""

import os
import csv
import time
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
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


# Load the 'hate' subset of the TweetEval dataset
dataset = load_dataset('tweet_eval', 'hate')

# Extract the tweet texts from the dataset's training split
train_split = dataset['train']
tweet_texts =train_split['text']
tweet_labels = train_split['label'] # 0: Non-hate, 1: Hate

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
    
# Define batch size
batch_size = 1000

# Process tweets in batches
for batch_start in range(0, len(tweet_texts), batch_size):
    batch_end = min(batch_start + batch_size, len(tweet_texts))
    batch_tweets = tweet_texts[batch_start:batch_end]
    batch_labels = tweet_labels[batch_start:batch_end]

    results = []

    for idx, (tweet, label) in enumerate(tqdm(zip(batch_tweets, batch_labels), total=len(batch_tweets), desc=f"Processing batch {batch_start//batch_size+1}")):
        # print(f'Processing tweet {batch_start+idx}/{len(tweet_texts)}...')
        # Perform sentiment analysis
        sentiment, sentiment_score = analyze_sentiment(tweet)

        results.append({
            'Tweet': tweet,
            'Sentiment': sentiment,
            'Sentiment Score': sentiment_score,
            'Original Label': 'Hate' if label==1 else 'Non-hate'
        })
 
        # Add a delay to comply with OpenAI API rate limits
        time.sleep(2)  # Adjust the sleep time as needed

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Save the results to a CSV file
    path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/tweets/"
    batch_number = (batch_start//batch_size) + 1
    output_csv = f'tweet_{batch_size}_batch_{batch_number}_analysis_gpt4_with_sentiment.csv'
    results_df.to_csv(path + output_csv, index=False, encoding='utf-8')

    print(f"Batch {batch_start//batch_size + 1} results saved to {output_csv}")

    # Display a preview of results
    print(results_df.head())                

