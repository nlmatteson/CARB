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
# san diego data
test = 'city-san_diego-final.csv'
raw = pd.read_csv(root + test)
print(raw.columns.to_list())
# %% List Desired Fields

fields = ['approval_id', 'address_job', 'approval_type',
'date_approval_create', 'lng_job', 'lat_job', 'job_apn',
'date_approval_issue',
'date_approval_close', 'project_type', 'project_status',
'date_project_create', 'project_scope', 'project_title',
'approval_scope','approval_valuation','zip']

# %% Extract File for Testing
df = pd.read_csv(root + test, 
    usecols = fields, 
    header = 0,
    skiprows = [1],
    low_memory = False)

df.reset_index(drop = True, inplace = True)

#%%  Create Output Dataframe Structure
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
out_df['place'] = 'San Diego city'
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

'''def extract_zipcode(address):
    if isinstance(address, str):
        pattern = r'\b9\d{4}\b'  # Regex pattern to match ZIP code starting with 9
        match = re.search(pattern, address)
        if match:
            return match.group()
    return None''
'''
# Apply the function to the 'address' column and create a new 'zipcode' column
#out_df['zipcode'] = df['Address'].apply(extract_zipcode)

#get the first five digits so it doesn't add ".0"
out_df['zipcode'] = df['zip'].astype(str).str[:5]


out_df.head()

# %% Populate Permit Number Field
out_df['permit_number'] = df.loc[:,'approval_id']

#%% generate full description

df['full_desc']= (df['project_scope'].astype(str) +', '+ df['project_title'].astype(str) + ', ' + df['approval_scope'].astype(str))
# %% Populate Project Description Field
out_df['project_description'] = df.loc[:,'full_desc']

# %% Populate Permit Class Field
out_df['permit_type'] = df.loc[:,'approval_type']
# %% Populate Estimated Cost Field
out_df['estimated_cost'] = df['approval_valuation']

# %% Populate Applied Date Filed

out_df ['applied_date'] = df.loc[:,'date_project_create']

# %% Populate Issued Date Filed

out_df ['issued_date'] = df.loc[:,'date_approval_issue']

# %% Populate Completed Date Filed

out_df ['finaled_date'] = df.loc[:,'date_approval_close']

# %% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')
out_df['finaled_date'] = pd.to_datetime(out_df['finaled_date'], errors = 'coerce')


# %% Populate Address Feild

out_df['address'] = df.loc[:,'address_job']

# %% Popluate Coordinate Fields

out_df.loc[:,'latitude'] = df.loc[:,'lat_job']
out_df.loc[:,'longitude'] = df.loc[:,'lng_job']

# %% Populate Parcel Number
out_df.loc[:,'parcel_number'] = df.loc[:,'job_apn']

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
