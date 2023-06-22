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
# victorville
test = 'city-victorville-final.csv'
raw = pd.read_csv(root + test)
print(raw.columns.to_list())

# %% List Desired Fields
fields= ['PERMIT_NUMBER', 'MAIN_ADDRESS_LINE1', 'MAIN_ADDRESS_LINE2',
'PARCEL_NUMBER', 'PERMIT_TYPE', 'PERMIT_STATUS', 'WORK_CLASS',
'APPLICATION_DATE', 'ISSUE_DATE', 'FINALED_DATE',
'VALUATION', 'DESCRIPTION']

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
out_df['place'] = 'Victorville city'
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
out_df['zipcode'] = df['MAIN_ADDRESS_LINE2'].apply(extract_zipcode)
'''
#get the first five digits so it doesn't add ".0"
out_df['zipcode'] = df['ZIP_CODE'].astype(str).str[:5]
'''

out_df.head()

# %% Populate Permit Number Field
out_df['permit_number'] = df.loc[:,'PERMIT_NUMBER']

# %% Populate permit class

out_df['permit_class'] = df.loc[:,'WORK_CLASS']


# %% Populate permit type
out_df['permit_type'] = df.loc[:,'PERMIT_TYPE']

# %% Populate description
out_df['project_description']= df.loc[:,'DESCRIPTION']

# %% Populate Estimated Cost Field

out_df['estimated_cost'] = df['VALUATION']

# %% Populate Applied Date Filed

out_df ['applied_date'] = df.loc[:,'APPLICATION_DATE']

# %% Populate Issued Date Filed

out_df ['issued_date'] = df.loc[:,'ISSUE_DATE']

# %% Populate Completed Date Filed

out_df ['finaled_date'] = df.loc[:,'FINALED_DATE']

# %% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')
out_df['finaled_date'] = pd.to_datetime(out_df['finaled_date'], errors = 'coerce')


# %% Populate Parcel Number

out_df.loc[:,'parcel_number'] = df.loc[:,'PARCEL_NUMBER']

# %% combine address columns
df['address'] = (df['MAIN_ADDRESS_LINE1'].astype(str) + ', ' + df['MAIN_ADDRESS_LINE2'].astype(str))

# %% Populate address
out_df['address'] = df.loc[:,'address']
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
