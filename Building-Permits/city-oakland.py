#%% Package Imports

import pandas as pd
import numpy as np
import datetime as dt
import os

# %% Set Working Directory
root = "V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\2_working-files\\"
os.chdir(root)
files = os.listdir()

# %% Read In Raw Table
# oakland data
test = 'city-oakland-final.csv'
raw = pd.read_csv(root + test)
print(raw.columns.to_list())

# %%  List Desired Fields
fields = ['File Date', 'Status', 'Record Number', 'Record Type',
'Address', 'Description', 'Short Notes']
# %% Extract File for Testing

df = pd.read_csv(root + test, 
    usecols = fields, 
    header = 0,
    skiprows = [1],
    low_memory = False)

df.reset_index(drop = True, inplace = True)

# %% Create Output Dataframe Structure

cols = [
    'permit_number',
    'project_description',
    'permit_class',
    'permit_type',
    'estimated_cost',
    'applied_date',
    'issued_date',
    'finaled_date',
    'address',
    'parcel_number',
    'latitude',
    'longitude',
    'place',
    'county_name',
    'zipcode',
    'file_name']

out_df = pd.DataFrame(index = df.index,
    columns = cols)

#%% Format city or county fields
out_df['place'] = 'Oakland city'
#%% populate zipcode field
import re 

# Function to extract zip code using regular expression
#This code snippet uses the re.findall() function to find a pattern of five consecutive digits 
# (\d{5}) in the address string. It extracts the first occurrence of such a pattern as the zip code. 
# If no zip code is found, it assigns None to the 'zipcode' column.
'''def extract_zipcode(address):
    if isinstance(address, str):
        zipcode = re.findall(r'\b\d{5}\b', address)
        if zipcode:
            return zipcode[0]
    return None
'''
def extract_zipcode(address):
    if isinstance(address, str):
        pattern = r'\b9\d{4}\b'  # Regex pattern to match ZIP code starting with 9
        match = re.search(pattern, address)
        if match:
            return match.group()
    return None

# Apply the function to the 'address' column and create a new 'zipcode' column
out_df['zipcode'] = df['Address'].apply(extract_zipcode)
'''
#get the first five digits so it doesn't add ".0"
out_df['zipcode'] = df['ZIP_CODE'].astype(str).str[:5]
'''

out_df.head()
# %% Creating full description column that combines Description and Short Notes

df['full_desc']= (df['Description'].astype(str) + ',' + df['Short Notes'].astype(str))
# %% Populate Permit Number

out_df['permit_number'] = df.loc[:,'Record Number']

# %% Populate Project Description Field

out_df['project_description'] = df.loc[:,'full_desc']

# %% Populate Permit Class Field

out_df['permit_type'] = df.loc[:,'Record Type']

#%% Populate Applied Date Filed

out_df ['applied_date'] = df.loc[:,'File Date']


# %% Populate Address field

out_df['address'] = df.loc[:,'Address']

# %% ormate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')

# %% Populate File Name

out_df['file_name'] = test


#%% drop duplicates
print(len(out_df))
out_df=out_df.drop_duplicates()
print(len(out_df))

# %% Output to Clean CSV File

out_root = 'V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\3_permit-processing\\'
out_df.to_csv( out_root + os.path.splitext(test)[0] + '_may-update.csv')

# %%
