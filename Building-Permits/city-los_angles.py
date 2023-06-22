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
# los angeles
test = 'city-los_angeles-final.csv'
raw = pd.read_csv(root + test)
print(raw.columns.to_list())
# %% List Desired Fields

fields = ['PERMIT_NBR', 'PRIMARY_ADDRESS', 'ZIP_CODE',
'APN', 'GROUP', 'PERMIT_TYPE', 'PERMIT_SUB_TYPE',
'USE_CODE', 'USE_DESC','SUBMITTED_DATE', 'ISSUE_DATE',
'STATUS', 'TYPE_LAT_LON', 'LAT', 'LON', 'WORK_DESC']

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

out_df['place'] = 'Los Angeles city'
#%% populate zipcode field
'''import re 

# Function to extract zip code using regular expression
#This code snippet uses the re.findall() function to find a pattern of five consecutive digits 
# (\d{5}) in the address string. It extracts the first occurrence of such a pattern as the zip code. 
# If no zip code is found, it assigns None to the 'zipcode' column.
def extract_zipcode(address):
    if isinstance(address, str):
        zipcode = re.findall(r'\b\d{5}\b', address)
        if zipcode:
            return zipcode[0]
    return None

# Apply the function to the 'address' column and create a new 'zipcode' column
out_df['zipcode'] = df['Address'].apply(extract_zipcode)
'''
#get the first five digits so it doesn't add ".0"
out_df['zipcode'] = df['ZIP_CODE'].astype(str).str[:5]


out_df.head()

# %% Populate Permit Number Field

out_df['permit_number'] = df.loc[:,'PERMIT_NBR']

# %% Populate Project Description Field

out_df['project_description'] = df.loc[:,'WORK_DESC']

# %% Populate Permit Class Field

out_df['permit_class'] = df.loc[:,'PERMIT_SUB_TYPE']

# %% Populate Permit Class Field

out_df['permit_type'] = df.loc[:,'PERMIT_TYPE']

#%% Populate Applied Date Filed

out_df ['applied_date'] = df.loc[:,'SUBMITTED_DATE']

# %% Populate Issued Date Filed

out_df ['issued_date'] = df.loc[:,'ISSUE_DATE']

# %% Populate Address Feild

df['full_address'] = (df['PRIMARY_ADDRESS'].astype(str) + ' ' + df['ZIP_CODE'].astype(str))
out_df['address'] = df.loc[:,'full_address']

# %% Populate Parcel Number

out_df.loc[:,'parcel_number'] = df.loc[:,'APN']

#%% Populate File Name

out_df['file_name'] = test

# %% Populate Coordinate Fields

out_df.loc[:,'latitude'] = df.loc[:,'LAT']
out_df.loc[:,'longitude'] = df.loc[:,'LON']

# %% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')


#%% drop duplicates
print(len(out_df))
out_df=out_df.drop_duplicates()
print(len(out_df))

# %% Output to Clean CSV File

out_root = 'V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\3_permit-processing\\'
out_df.to_csv( out_root + os.path.splitext(test)[0] + '_may-update.csv')



# %%
