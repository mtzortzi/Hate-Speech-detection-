#!/usr/bin/python3

"""
    scrapes the greek newspaper "athinorama"
    
    @author mtzortzi
"""


import os
import csv
import time # Import time module for delays
import pandas as pd
from bs4 import BeautifulSoup

# Number of words to extract for preview
numwords = 100
newspaper = 'athinorama'
# Stop phrase
stop_phrase = "Δείτε όλες τις εκθέσεις της πόλης στον"


# Define the folder path containing the HTML files and the output CSV file
folder_path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/webpages_html/Greek/athinorama"
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
        title = soup.find('h1').text.strip() if soup.find('h1') else "No Title Found"
        
        # Find all content blocks
        content_blocks = soup.find('div', class_='article-content')  # Adjust the class as per your HTML structure
        article_text = ""
        if content_blocks:
            # Remove unwanted elements 
            for unwanted in content_blocks.find_all(['div', 'script'], class_=['image', 'related-story']):
                unwanted.decompose()
    
            # Iterate through children of article-content
            for element in content_blocks.children:
                # Stop if <div class="review-content"> is encountered
                if isinstance(element, str):  # Skip string elements
                    continue
                if element.name == "div" and "review-content" in element.get("class", []):
                    break  # Stop extracting content

                # If it's a paragraph, add its text
                if element.name == "p":
                    # Check for stop phrase inside <em> tags
                    for em in element.find_all('em'):
                        if stop_phrase in em.get_text(strip=True):
                            break # Stop processing further
                    else:
                        # If stop phrase not found, add paragraph text
                        article_text += element.get_text(separator=" ", strip=True) + " "

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
