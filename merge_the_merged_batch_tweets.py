#!/usr/bin/python3

"""
   merge the merged_batch_i for tweet files into one. 
    @author mtzortzi
"""

import os
import pandas as pd

# Define the folder path where the merged batch files are located
folder_path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/tweets"

# List all merged batch files in the folder
merged_files = sorted([f for f in os.listdir(folder_path) if f.startswith("merged_batch_") and f.endswith(".csv")])

# Initialize an empty list to store dataframes
dataframes = []

# Load each CSV file into a dataframe and append to the list
for file in merged_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, encoding="utf-8")
    dataframes.append(df)

# Concatenate all dataframes into one
final_merged_df = pd.concat(dataframes, ignore_index=True)

# Save the final merged file
output_path = os.path.join(folder_path, "final_merged_batches.csv")
final_merged_df.to_csv(output_path, index=False, encoding="utf-8")

print(f"✔ Final merged file saved as: {output_path}")
