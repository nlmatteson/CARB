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
# tulare county
test = 'county-tulare-final.csv'
raw = pd.read_csv(root + test)
print(raw.columns.to_list())

# %% List Desired Fields
fields= ['Case Number', 'Type', 'Status', 'Project Name',
'Issued Date', 'Applied Date', 'Finalized Date',
'Address', 'Main Parcel', 'Description']

# %% Extract File for Testing
df = pd.read_csv(root + test, 
    usecols = fields, 
    header = 0,
    skiprows = [1],
    low_memory = False)

df.reset_index(drop = True, inplace = True)
# %%Create Output Dataframe Structure
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
out_df['county_name'] = 'Tulare County'
#%% populate zipcode field
import re 

# Function to extract zip code using regular expression

def extract_zipcode(address):
    if isinstance(address, str):
        pattern = r'\b9\d{4}\b'  # Regex pattern to match ZIP code starting with 9
        match = re.search(pattern, address)
        if match:
            return match.group()
    return None

# Apply the function to the 'address' column and create a new 'zipcode' column
out_df['zipcode'] = df['Address'].apply(extract_zipcode)

out_df.head()

# %% Populate Permit Number Field
out_df['permit_number'] = df.loc[:,'Case Number']

#%% populate permit type
out_df['permit_type'] = df.loc[:,'Type']
# %% populate description
out_df['project_description']= df.loc[:,'Description']

# %%  Populate Applied Date Filed
out_df ['applied_date'] = df.loc[:,'Applied Date']

# %% Populate Issued Date Filed
out_df ['issued_date'] = df.loc[:,'Issued Date']

# %% Populate Completed Date Filed
out_df ['finaled_date'] = df.loc[:,'Finalized Date']

# %% Formate Date Fields
out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')
out_df['finaled_date'] = pd.to_datetime(out_df['finaled_date'], errors = 'coerce')

# %% Populate Address Feild
out_df['address'] = df.loc[:,'Address']

#%% Populate parcel
out_df['parcel_number']= df.loc[:,'Main Parcel']

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
