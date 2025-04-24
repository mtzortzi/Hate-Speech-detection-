#!/usr/bin/python3

"""
    scrapes the spanish newspaper "el_diario"
    
    @author mtzortzi
"""


import os
import csv
import json
import time # Import time module for delays
import pandas as pd
from bs4 import BeautifulSoup

newspaper = 'eldiario'
numwords = 100


# Define the folder path containing the HTML files and the output CSV file 
folder_path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/webpages_html/Spanish/El_Diario"
output_path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/Spanish/"
output_csv = output_path + "all_articles_combined_" + newspaper + ".csv"
os.makedirs(output_path, exist_ok=True)

# Prepare a list to store data from all files
all_data = []

# Loop through all files in the specified folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".html"):  # Only process HTML files

        print(f'Processing file: {file_name}')
        # Introduce a delay of 2 seconds between processing each file
        time.sleep(2)

        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract the title and article text
        title = soup.title.string if soup.title else "No Title Found"
        article_body = soup.find("script", type="application/ld+json")
        if article_body:
            try:
                article_data = json.loads(article_body.string)
                article_text = article_data.get("articleBody", "No Article Text Found")
            except json.JSONDecodeError:
                article_text = "Error decoding articleBody"
        else:
            article_text = "No Article Text Found"
        
        # Extract the first and last `numwords` words
        words = article_text.split()
        first_words = " ".join(words[:numwords]) if len(words) >= numwords else " ".join(words)
        last_words = " ".join(words[-numwords:]) if len(words) >= numwords else " ".join(words)
        
        # Append to the data list
        all_data.append({
            "File Name": file_name,
            "Title": title,
            "Text": article_text,
            "First Words": first_words,
            "Last Words": last_words
        })


# Convert the data to a DataFrame with proper column names
df_all = pd.DataFrame(all_data, columns=["File Name","Title", "Text", "First Words", "Last Words"])

# Save all data to a single CSV file
df_all.to_csv(output_csv, index=False, sep=',', quoting=csv.QUOTE_ALL, encoding='utf-8')

# Print a preview of the extracted data
for article in all_data:
    print(f"File: {article['File Name']}")
    print(f"Title: {article['Title']}")
    print(f"Text: {article['Text'][:200]}...")  # Preview of the first 200 characters
    print(f"First {numwords} words: {article['First Words']}")
    print(f"Last {numwords} words: {article['Last Words']}")
    print("-" * 50)
