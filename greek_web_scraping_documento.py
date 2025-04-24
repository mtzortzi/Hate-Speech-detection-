#!/usr/bin/python3

"""
    scrapes the greek newspaper "documento"
    
    @author mtzortzi
"""

import os
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup

# Number of words to extract for preview
numwords = 100
newspaper = 'documento'

# Define the folder path containing the HTML files and the output CSV file
folder_path = r"C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/webpages_html/Greek/documento/"
output_path = r"C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/Greek/"
output_csv = os.path.join(output_path, f"all_articles_combined_{newspaper}.csv")
os.makedirs(output_path, exist_ok=True)

# Print all files in the directory
print("Files in directory:")
file_list = os.listdir(folder_path)
for file_name in file_list:
    print(file_name)

# Prepare a list to store data from all files
all_data = []

# Loop through all files in the specified folder
for file_name in file_list:
    print(f'--------------------------------------------------------------------')
    if file_name.endswith(".html"):  # Only process HTML files
        print(f'Processing file: {file_name}')

        # Introduce a delay of 2 seconds between processing each file
        time.sleep(2)

        file_path = os.path.join(folder_path, file_name)

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except UnicodeDecodeError:
            print(f"⚠️ Encoding error for {file_name}. Retrying with 'latin1'...")
            with open(file_path, 'r', encoding='latin1') as file:
                html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Locate the main article content
        entry_content = soup.find("div", class_="entry-content")
        if entry_content:
            article_text = entry_content.get_text(separator="\n", strip=True)

            # Clean text and split
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
        else:
            print("Main article content not found.")
            continue

# Convert the data to a DataFrame
df_all = pd.DataFrame(all_data, columns=['File Name', 'Title', 'Text', 'First Words', 'Last Words'])

# Save all data to a single CSV file
df_all.to_csv(output_csv, index=False, sep=',', quoting=csv.QUOTE_ALL)

# Print a preview of the extracted data
for article in all_data:
    print("=" * 50)
    print(f"File: {article['File Name']}")
    print(f"Title: {article['Title']}")
    print(f"Text: {article['Text'][:200]}... \n")  # Preview of the first 200 characters
    print(f"First {numwords} words: {article['First Words']} \n")
    print(f"Last {numwords} words: {article['Last Words']}")