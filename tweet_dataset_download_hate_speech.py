#!/usr/bin/python3

"""
    download and save the text of tweets labeled for hate speech from the TweetEval dataset
    
    @author mtzortzi
"""

from datasets import load_dataset

# Load the 'hate' subset of the TweetEval dataset
dataset = load_dataset('tweet_eval', 'hate')
# Access the training split
train_split = dataset['train']

# Extract tweet texts
tweet_texts = train_split['text']

# Display the first 5 tweets
for tweet in tweet_texts[:5]:
    print(tweet)

# Define the output file path
output_file = 'hate_tweets.txt'


path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/tweets/"
# Write tweet texts to the file
with open(path+output_file, 'w', encoding='utf-8') as f:
    for tweet in tweet_texts:
        f.write(tweet + '\n')
