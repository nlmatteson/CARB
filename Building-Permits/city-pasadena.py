#%% Package Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import datetime as dt
import os

# %% Set Working Directory
root = "V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\2_working-files\\"
os.chdir(root)
files = os.listdir()

# %% Read In Raw Table
# pasadena data
test = 'city-pasadena-final.geojson'

#%% geojson file
raw = gpd.read_file(root + test)

#%% getting columns
print(raw.columns.to_list())

# %% List Desired Fields

fields = ['PARCEL_NO', 'ADDRESS', 'CASE_NUMBER',
'DESCRIPTION', 'TOTAL_SQFT', 'LATEST_ACTIVITY', 'PID', 'geometry']

# %% Extract File for Testing

df = gpd.read_file (root + test, 
    fields = fields, 
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
out_df['place'] = 'Pasadena city'
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
out_df['zipcode'] = df['ADDRESS'].apply(extract_zipcode)
'''
#get the first five digits so it doesn't add ".0"
out_df['zipcode'] = df['ZIP_CODE'].astype(str).str[:5]
'''

out_df.head()
# %% Populate Permit Number Field

out_df['permit_number'] = df.loc[:,'CASE_NUMBER']

# %% Populate Project Description Field

out_df['project_description'] = df.loc[:,'DESCRIPTION']

# %% Date field is actually the latest activity in time/date format

out_df ['applied_date'] = df.loc[:,'LATEST_ACTIVITY']

# %% Populate Address Field

out_df['address'] = df.loc[:,'ADDRESS']

# %% Generate Lat and Lon column from point geometry

df['lon'] = df['geometry'].x
df['lat'] = df['geometry'].y

# %% Popluate Coordinate Fields

out_df.loc[:,'latitude'] = df.loc[:,'lat']
out_df.loc[:,'longitude'] = df.loc[:,'lon']



# %% POPULATE APN

out_df['parcel_number'] = df.loc[:,'LAND_PARCEL_NO']

# %% Formate Date Fields

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
