#!/usr/bin/python3

"""
    calls chatgpt with a prompt to classify for racial hate speech against Black individuals and assess the author's motivation
    
    @author mtzortzi
"""

import re
import io
import csv
import time
import openai
import pandas as pd

# Load the CSV file
path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/"

country = 'Greek' #'Spanish'#'Greek'#'Italian' #'Spanish' #'Greek'  # Replace with the desired country
newspaper = 'ladylike' #'elplural'#'documento'#'provocateur'#'ertnews'#'skai'#'popaganda'#'tanea'#'lifo'#'internazionale'#'openmigration' #'ansa' #'openpolis'#'il_giornale' #'il_fatto_quotidiano' #'eldiario' #'kathimerini' #'athinorama' #'kathimerini' #'proto_thema' #'elpais' #'eldiario' # Replace with the desired newspaper

df = pd.read_csv(path + country + '/' + 'sentiment_analysis_' + newspaper + '.csv')

prompt = """
     Goal:
    You are a political scientist with profound expertise in hate speech and discrimination. You are given the following newspaper article. Your task is to determine:

        1. Whether the article contains racial hate speech against People of African Descent (Black people).
        2. Whether the motivation of the author of the article is racist.
    Return Format:
        Provide your answers in the following CSV format:

        Yes or No, Explanation of the first answer without any punctuation, Yes or No, Explanation of the second answer without any punctuation

        Ensure that your response strictly follows this format, using commas to separate each element, and omitting all punctuation marks in the explanations.

    Warnings:

        If the author's motivation is No, then there must be No hate speech.
        If the author's motivation is Yes, then there must be Yes to hate speech.
    """

# OpenAI API Key
openai.api_key = "OPEN AI API KEY"

def ask_gpt(text, prompt):
    try:

        # Step 0: Handle missing article text
        if not text or text == "" or text == 'No Article Text Found':
            print("⚠️ Skipping empty article text.")
            return "Error", "No article text provided", "Error", "No article text provided"

        # GPT Request
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )

        response_text = response.choices[0].message.content.strip()

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
            print(f'inside after the position is 2')
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

# Initialize a list to store responses
responses = []

# Iterate over each row in the DataFrame
for idx, row in df.iterrows():
    text = row['Text']
    print(f"Processing row {idx + 1}/{len(df)}...")
    # print(f"text from dataframe is: \n {text}")
    response = ask_gpt(text, prompt)
    print(f'show me for article {idx} the response {response}')
    print("------------------------------------------------------------------------------")
    responses.append(response)
    # Add a delay to comply with API rate limits
    time.sleep(1)

# Convert responses into DataFrame columns
df["Racial_Hate_Speech"], df["Explanation_Hate_Speech"], df["Motivation_Author"], df["Explanation_Motivation"] = zip(*responses)

# Save the updated DataFrame to a new CSV
output_path = f"{path}{country}/chatgpt_classification_{newspaper}.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Results saved to {output_path}")

###################### Display the targeted columns ##############################
# Define the columns you want to display
columns_to_display = ["Title", "Racial_Hate_Speech", "Explanation_Hate_Speech", "Motivation_Author", "Explanation_Motivation"]

# Check if all specified columns exist in the DataFrame
missing_columns = [col for col in columns_to_display if col not in df.columns]
if missing_columns:
    print(f"Warning: The following columns are missing from the DataFrame: {missing_columns}")
else:
    # Create a new DataFrame with only the specified columns
    df_selected = df[columns_to_display]

    # Print the new DataFrame
    print(df_selected)