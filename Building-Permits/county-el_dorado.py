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
# el dorado county
test = 'county-el_dorado-final.csv'
raw = pd.read_csv(root + test)
print(raw.columns.to_list())

# %% List Desired Fields
fields= ['PERMIT_NO', 'APPLIED', 'Permit Type', 
'Permit Sub Type',
'SITE_APN', 'SITE_ADDR', 'APPLICANT_NAME', 'RECORDID']

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
out_df['county_name'] = 'El Dorado County'
#%% populate zipcode field
# need to import regex

import re 

# Function to extract zip code using regular expression
# If no zip code is found, it assigns None to the 'zipcode' column.

def extract_zipcode(address):
    if isinstance(address, str):
        pattern = r'\b9\d{4}\b'  # Regex pattern to match ZIP code starting with 9 followed by 4 digits
        match = re.search(pattern, address)
        if match:
            return match.group()
    return None

# Apply the function to the 'address' column and create a new 'zipcode' column
out_df['zipcode'] = df['SITE_ADDR'].apply(extract_zipcode)

#checking to make sure it works
out_df.head()

# %% Populate Permit Number Field
out_df['permit_number'] = df.loc[:,'RECORDID']

# %% Populate permit class

out_df['permit_class'] = df.loc[:,'Permit Type']

#%% populate permit type

out_df['permit_type'] = df.loc[:,'Permit Sub Type']

# %% populate description
out_df['project_description']= df.loc[:,'Permit Sub Type']

# %% Populate  Date Fieled

out_df ['applied_date'] = df.loc[:,'APPLIED']

# %% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')

# %% Populate Address Feild
out_df['address'] = df.loc[:,'SITE_ADDR']

# %% POPULATE parcel number
out_df['parcel_number'] = df.loc[:,'SITE_APN']

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
