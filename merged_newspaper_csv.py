#!/usr/bin/python3

"""
    This script merges all CSV files in a specified folder that start
    with "chatgpt_classification_", adds a "newspaper" column with the 
    newspaper name extracted from the filename, a "Country" column based
    on the folder name, and saves the final dataset as "{country}_merged_newspaper_analysis.csv".

    @author mtzortzi
"""

import os
import pandas as pd

# Define the language
language = 'Greek'#'Spanish'#'Greek'#'Italian' #'Spanish' #'Greek'  # Change this if needed

# Define the base path
path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/"
folder_path = os.path.join(path, language)

# Check if the folder exists
if not os.path.exists(folder_path):
    print(f"Error: The specified folder does not exist: {folder_path}")
    exit(1)

# Determine country based on folder name
country_mapping = {
    "Greek": "Greece",
    "Spanish": "Spain",
    "Italian": "Italy"
}
country = country_mapping.get(language, "Unknown")

# List all CSV files in the folder matching the naming pattern
csv_files = [f for f in os.listdir(folder_path) if f.startswith("chatgpt_classification_") and f.endswith(".csv")]

if not csv_files:
    print(f"No CSV files found in {folder_path} matching the pattern 'chatgpt_classification_*.csv'")
    exit(1)

# Load and process each CSV file
dataframes = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(file_path, encoding="utf-8")  # Read CSV with UTF-8 encoding
        if df.empty:
            print(f"Warning: {file} is empty and will be skipped.")
            continue
        
        # Extract newspaper name from filename
        newspaper_name = file.replace("chatgpt_classification_", "").replace(".csv", "")
        df["newspaper"] = newspaper_name
        df["Country"] = country  # Add country column
        dataframes.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")
        continue  # Skip the file and continue processing

# Merge all dataframes
if not dataframes:
    print("No valid data found in the CSV files. Exiting.")
    exit(1)

merged_df = pd.concat(dataframes, ignore_index=True)

# Save the merged dataframe to a new CSV file
output_filename = f"{country}_merged_newspaper_analysis.csv"
output_path = os.path.join(folder_path, output_filename)
merged_df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Merged file successfully saved as: {output_path}")