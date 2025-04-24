#!/usr/bin/python3

"""


    In this dataset, labels are typically:
    - 0: Not hateful
    - 1: Hateful

    - Pre-trained model: cardiffnlp/twitter-roberta-base-hate-latest
    It has been trained on a combination of 13 different hate speech
    datasets in the English language, encompassing various forms of hate speech, including those targeting race.

    -  The model has been exposed to various hate speech forms, which likely include instances of racial hate speech against Black individuals.
    
    @author mtzortzi
"""

import csv
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification 

# Load pre-trained model and tokenizer
model_name = 'cardiffnlp/twitter-roberta-base-hate'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define classification function
def classify_tweet(tweet):
    inputs = tokenizer(tweet, return_tensors='pt')
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    hate_score = probabilities[0][1].item() # Score for the 'hateful' label

    # Thresholds can be adjusted based on desired sensitivity
    hate_speech = 'yes' if hate_score > 0.5 else 'no'
    motivation = 'yes' if hate_score > 0.7 else 'no' 

    return hate_speech, motivation


# Load the 'hate' subset of the TweetEval dataset
dataset = load_dataset('tweet_eval', 'hate')

# Access the training split
train_split = dataset['train']

# Extract tweet texts and labels
tweet_texts = train_split['text']
labels = train_split['label']

# Define the output csv file path
path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/"
output_csv = path + '/' + 'tweet_analysis' + '.csv'

# Open the csv file for writing
with open (output_csv, mode='w', newline = '', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Racial Hate Speech', 'Explanation', 'Motivation of the Author', 'Explanation'])

    # Analyze each tweet
    for tweet in tweet_texts:
        hate_speech, motivation = classify_tweet(tweet)
        # Placeholder explanations
        hate_speech_explanation = "Contains racial slurs" if hate_speech == 'yes' else 'No racial content'
        motivation_explanation = 'Language indicates racial bias' if motivation == 'yes' else 'No evident racial bias'
        # Write the analysis to the csv
        writer.writerow([hate_speech, hate_speech_explanation, motivation, motivation_explanation])