#!/usr/bin/python3

"""
    scrapes the greek newspaper "proto_thema"
    
    @author mtzortzi
"""


import os
import csv
import time # Import time module for delays
import pandas as pd
from bs4 import BeautifulSoup

# Number of words to extract for preview
numwords = 100
newspaper = 'proto_thema'

# Define the folder path containing the HTML files and the output CSV file
folder_path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/webpages_html/Greek/"
output_path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/Greek/"
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
            html_content = file.read()
        
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove all elements with the class `cookies`
        for cookies_element in soup.find_all(class_='cookies'):
            cookies_element.decompose()  # Removes the element entirely
        
        # Extract the title
        title = soup.find('title').text.strip() if soup.find('title') else "No Title Found"
        
        # Find all content blocks
        content_blocks = soup.find_all('div', class_='cnt')  # Adjust the class as per your HTML structure
        article_text = ""
        if content_blocks:
            for block in content_blocks:
                # Remove unwanted sections within the content container
                for unwanted in block.find_all(['aside', 'footer', 'nav', 'div'], class_=['advertisement', 'related-articles', 'comment', 'articleContainer_mainLeft', 'cookies','outer']):
                    unwanted.decompose()

                stop_element = block.find('div', class_='articleContainer_mainLeft')
                if stop_element:
                    print('inside')
                    break # Stop processing further content blocks

                # Extract text up to the stop element
                content_up_to_stop = ""
                for child in block.children:
                    # Check if the child is the stop element
                    if hasattr(child, 'get_text') and child.get_text(strip=True) == "Ειδήσεις σήμερα:":
                        break  # Stop processing further content blocks
                    # Otherwise, add the text of the child
                    if hasattr(child, 'get_text'):
                        content_up_to_stop += child.get_text(separator=" ", strip=True) + " "


                # Append the processed text of the block
                article_text += content_up_to_stop.strip() + " "
            
            article_text = article_text.strip()  # Remove extra whitespace
        else:
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
df_all.to_csv(output_csv, index=False, sep=',', quoting=csv.QUOTE_ALL)#, encoding='utf-8')

# Print a preview of the extracted data
for article in all_data:
    print(f"File: {article['File Name']}")
    print(f"Title: {article['Title']}")
    print(f"Text: {article['Text'][:200]}... \n")  # Preview of the first 200 characters
    print(f"First {numwords} words: {article['First Words']} \n")
    print(f"Last {numwords} words: {article['Last Words']}")
    print("-" * 50)
