#!/usr/bin/python3

"""

    Convert csv file into excel    

    @author mtzortzi
"""

import csv
import time
import pandas as pd

# Load the CSV file
path = "C:/Users/MariaΙoannaTzortzi/OneDrive - ITML/AFRO_EQUALITY/New_Attempt/Datasets/"

language = 'Greek'
country = 'Greece'

# language = 'Spanish'
# country = 'Spain'

df = pd.read_csv(path + language + '/' + country + '_merged_newspaper_analysis' + '.csv')

print(df.head())

excel_file = country + "_merged_newspaper_analysis.xlsx"

df.to_excel(path + language + '/' + excel_file, index=False, engine='openpyxl')

print(f"✅ CSV file successfully saved as {excel_file}")