#!/usr/bin/python3

"""

    Instructions for the prompt:
    1. Goal – Clearly define what you want.
    2. Return Format – Specify how you want the response structured.
    3. Warnings – Set accuracy guardrails.
    4. Context Dump – Provide background info for better results.


    calls chatgpt with a prompt to classify for racial hate speech against Black individuals and assess the author's motivation
    dataset: hate speech from the TweetEval dataset
    
    @author mtzortzi
"""

import re
import time
import openai
from tqdm import tqdm
import pandas as pd
from datasets import load_dataset

# Load the 'hate' subset of the TweetEval dataset
dataset = load_dataset('tweet_eval', 'hate')

# Extract the tweet texts from the dataset's training split
train_split = dataset['train']
tweet_texts =train_split['text']
tweet_labels = train_split['label'] # 0: Non-hate, 1: Hate

prompt = """
        ## Goal:
        You are a political scientist with expertise in hate speech and discrimination. Your task is to analyze the following tweet and determine:

        1. Whether the tweet contains racial hate speech against People of African Descent (Black people).
        2. Whether the author's motivation for writing the tweet is hateful or racist.

        ## Return Format:
        Your response must strictly follow this format:
        Yes or No, Explanation of the first answer without any punctuation, Yes or No, Explanation of the second answer without any punctuation

        - Separate each part with a comma.
        - The explanations should not contain any punctuation (periods, commas, colons, etc.).
        - Provide concise but clear reasoning.

        ## Warnings:
        - Do not include extra text outside of the required format.
        - If the tweet is neutral or unclear, classify it as "No" with a clear justification.
        - Avoid assumptions beyond what is explicitly stated in the tweet.
    """


# OpenAI API Key
openai.api_key = "OPEN AI API KEY"


# Function to send text to GPT-4 with a specific prompt
def classify_tweet_with_gpt4(tweet):

    try:
        
        # Handle empty or missing tweet text
        if not tweet or tweet.strip() == "":
            print("⚠️ Skipping empty tweet text.")
            return ["Error", "No tweet text provided", "Error", "No tweet text provided"]

        # Combine the text with the prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n\nTweet: \"{tweet}\""}
        ]
        
        # Call GPT-4 API using the latest structure
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100,  # Adjust based on desired response length - Prevents GPT from generating excessive explanations
            temperature=0.5 # Low randomness ensures more structured responses.
        )
        

        response_text = response.choices[0].message.content.strip()
    
        # Debugging: Show raw response from GPT
        # print(f"Raw GPT Response: {response_text}")

        # Step 1: Remove all elements before the first "Yes" or "No"
        match = re.search(r'\b(Yes|No)\b', response_text, re.IGNORECASE)

        if match:
            response_text = response_text[match.start():].strip()
        else:
            print(f"Unexpected response format (No Yes/No found): {response_text}")
            return "Error", "Error processing", "Error", "Error processing"

        # Step 2: Extract "Yes"/"No" responses
        yes_no_matches = re.findall(r'\b(Yes|No)\b', response_text, re.IGNORECASE)

        racial_hate = yes_no_matches[0] if len(yes_no_matches) > 0 else "Error"
        motivation = yes_no_matches[1] if len(yes_no_matches) > 1 else "Error"

        # Step 3: Find exact positions of "Yes" or "No" in text
        positions = [m.start() for m in re.finditer(r'\b(Yes|No)\b', response_text, re.IGNORECASE)]

        if len(positions) >= 2:
            # print(f'inside after the position is 2')
            explanation_start = positions[0] + len(racial_hate)  # After first "Yes" or "No"
            explanation_mid = positions[1]  # Start of second "Yes" or "No"
            explanation_end = positions[1] + len(motivation)  # After second "Yes" or "No"

            # Extract explanations
            reason_hate = response_text[explanation_start:explanation_mid].strip()
            reason_motivation = response_text[explanation_end:].strip()

            # Step 4: Handle cases where explanations failed to extract
            if not reason_hate or reason_hate.lower().startswith("yes") or reason_hate.lower().startswith("no"):
                print(f"⚠️ Issue detected in extracting first explanation: {reason_hate}")
                reason_hate = response_text[explanation_start:].split(motivation, 1)[0].strip()

            if not reason_motivation or reason_motivation.lower().startswith("yes") or reason_motivation.lower().startswith("no"):
                print(f"⚠️ Issue detected in extracting second explanation: {reason_motivation}")
                remaining_text = response_text[explanation_end:].strip()
                reason_motivation = remaining_text if remaining_text else "Error extracting second explanation"

        else:
            reason_hate, reason_motivation = "Error extracting explanation", "Error extracting explanation"

        return racial_hate, reason_hate, motivation, reason_motivation

    except Exception as e:
        print(f"Error processing text: {e}")
        return "Error", "Error processing", "Error", "Error processing"


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
        classification = classify_tweet_with_gpt4(tweet)
        results.append({
            'Tweet': tweet,
            'Hate Speech Detected': classification[0],
            'Explanation (Hate Speech)': classification[1],
            'Motivation of the Author': classification[2],
            'Explanation (Motivation)': classification[3],
            'Original Label': 'Hate' if label == 1 else 'Non-hate'
        })
 
        # Add a delay to comply with OpenAI API rate limits
        time.sleep(2)  # Adjust the sleep time as needed

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Save the results to a CSV file
    path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/tweets/"
    batch_number = (batch_start//batch_size) + 1
    output_csv = f'tweet_{batch_size}_batch_{batch_number}_analysis_gpt4_not_taking_account_the_label.csv'
    results_df.to_csv(path + output_csv, index=False, encoding='utf-8')

    print(f"Batch {batch_start//batch_size + 1} results saved to {output_csv}")

    # Display a preview of results
    print(results_df.head())                