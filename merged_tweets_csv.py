#!/usr/bin/python3

"""
    Merge the CSV output files from the tweet ChatGPT classification and the VADER sentiment analysis.  
    Ensures only one "Original Label" column is kept.  

    @author mtzortzi
"""

import os
import re
import pandas as pd

# Define the folder path where the CSV files are located
folder_path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/tweets"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# Dictionary to group files by batch number
batch_groups = {}

# Regular expression to extract batch number
pattern = re.compile(r"batch_(\d+)")

# Organize files based on batch numbers
for file in csv_files:
    match = pattern.search(file)
    if match:
        batch_number = match.group(1)
        if batch_number not in batch_groups:
            batch_groups[batch_number] = []
        batch_groups[batch_number].append(file)

# Merge files based on batch number
for batch, files in batch_groups.items():
    if len(files) == 2:  # Ensure we have exactly two files per batch
        file1, file2 = files
        file1_path = os.path.join(folder_path, file1)
        file2_path = os.path.join(folder_path, file2)

        # Load CSV files
        df1 = pd.read_csv(file1_path, encoding="utf-8")
        df2 = pd.read_csv(file2_path, encoding="utf-8")

        # Ensure "Tweet" column exists in both files
        if "Tweet" not in df1.columns or "Tweet" not in df2.columns:
            print(f"Skipping batch {batch}: 'Tweet' column missing in one of the files.")
            continue

        # Merge dataframes on the "Tweet" column
        merged_df = df1.merge(df2, on="Tweet", how="outer")

        # Identify "Original Label" columns
        original_label_columns = [col for col in merged_df.columns if "Original Label" in col]

        # Keep only the first "Original Label" column and drop others
        if original_label_columns:
            first_original_label = original_label_columns[0]  # Keep the first occurrence
            merged_df = merged_df.drop(columns=[col for col in original_label_columns if col != first_original_label])

        # Save merged file
        merged_filename = f"merged_batch_{batch}.csv"
        output_path = os.path.join(folder_path, merged_filename)
        merged_df.to_csv(output_path, index=False, encoding="utf-8")

        print(f"✔ Merged file saved as: {output_path}")
    else:
        print(f"⚠ Skipping batch {batch}: Expected 2 files, found {len(files)}.")
