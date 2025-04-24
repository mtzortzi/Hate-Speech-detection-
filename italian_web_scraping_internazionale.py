#!/usr/bin/python3

"""
    Scrapes the Italian newspaper "internazionale"
    
    @author mtzortzi
"""

import os
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup

# Number of words to extract for preview
numwords = 100
newspaper = 'internazionale'

# Define the folder path containing the HTML files and the output CSV file
folder_path = r"C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/webpages_html/Italian/internazionale"
output_path = r"C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/Italian/"
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

        # Remove all elements with the class `cookies`
        for cookies_element in soup.find_all(class_='cookies'):
            cookies_element.decompose()  # Removes the element entirely

        # Extract the title
        title = soup.find('h1').text.strip() if soup.find('h1') else "No Title Found"

        # Locate article content
        article_text = ""
        # Attempt to locate the correct container

        # Locate all divs with class 'content-grid'
        content_blocks = soup.find("div", class_="article-body")

        if content_blocks:
            print(f'✅ Found content grid')
            # Find all <div class="item_text"> and <div class="item_text dropcap">
            text_blocks = content_blocks.find_all('div', class_=['item_text', 'item_text dropcap'])

            if text_blocks:
                print(f'✅ Extracting text from {len(text_blocks)} content blocks in: {file_name}')
                # Extract text only from paragraph <p> tags inside each text block
                article_text = " ".join(
                    p.get_text(separator=" ", strip=True)
                    for block in text_blocks
                    for p in block.find_all('p')
                )
            else:
                print(f"❌ No <div class='item_text'> found inside <div class='article-body'> for: {file_name}")
                article_text = "Content found but structure mismatch"
        
        else:
            print(f"❌ Content container <div class='article-body'> not found for: {file_name}")
            article_text = "Content container not found"

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
df_all.to_csv(output_csv, index=False, sep=',', quoting=csv.QUOTE_ALL)

# Print a preview of the extracted data
for article in all_data:
    print("=" * 50)
    print(f"File: {article['File Name']}")
    print(f"Title: {article['Title']}")
    print(f"Text: {article['Text'][:200]}... \n")  # Preview of the first 200 characters
    print(f"First {numwords} words: {article['First Words']} \n")
    print(f"Last {numwords} words: {article['Last Words']}")