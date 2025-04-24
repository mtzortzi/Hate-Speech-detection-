#!/usr/bin/python3

"""
    scrapes the spanish newspaper "el_pais"
    
    @author mtzortzi
"""

import os
import csv
import json
import time # Import time module for delays
import pandas as pd
from bs4 import BeautifulSoup

newspaper = 'elpais'
numwords = 200


# Define the folder path containing the HTML files and the output CSV file 
folder_path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/webpages_html/Spanish/El_Pais"
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
        time.sleep(1)

        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the HTML
        soup = BeautifulSoup(content, 'html.parser')

        # Extract the title
        title = soup.find('title').text if soup.find('title') else "No title found"

        # Extract the main content inside <div class="a_c clearfix">
        main_content_div = soup.find('div', class_='a_c clearfix')
        if main_content_div:
            paragraphs = main_content_div.find_all('p')  # Find all <p> tags inside the main content
            article_text = ' '.join(p.get_text(separator=" ", strip=True) for p in paragraphs)  # Join paragraphs
        else:
            article_text = "Main content not found"
        
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


# Convert the data to a DataFrame
df_all = pd.DataFrame(all_data, columns=['File Name', 'Title', 'Text', 'First Words', 'Last Words'])

# Save all data to a single CSV file
df_all.to_csv(output_csv, index=False, sep=',', quoting=csv.QUOTE_ALL)#, encoding='utf-8')

# Print a preview of the extracted data
for article in all_data:
    print(f"File: {article['File Name']}")
    print(f"\n Title: {article['Title']} \n ")
    print(f"Text: {article['Text']}... \n")  # Preview of the first 200 characters
    # print(f"First {numwords} words: {article['First Words']} \n")
    # print(f"Last {numwords} words: {article['Last Words']}")
    print("-" * 50)
