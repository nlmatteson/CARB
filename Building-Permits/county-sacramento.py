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
# sacramento county
test = 'county-sacramento-final.geojson'
#%% its a geojson
raw = gpd.read_file(root + test)

#%%
print(raw.columns.to_list())

# %% List Desired Fields

fields = ['Application_Type', 'Application_Subtype',
'Application', 'Application_Status', 'OpenDate', 'APPLIED_DATE', 'ISSUED_DATE',
'FINALED_DATE', 'Parcel_Number', 'Address', 'ProjectName',
'Valuation','WorkDescription','geometry']

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
out_df['county_name'] = 'Sacramento County'
#%% populate zipcode field
import re 

# Function to extract zip code using regular expression
#This code snippet uses the re.findall() function to find a pattern of five consecutive digits 

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

# %%  Populate Permit Number Field
out_df['permit_number'] = df.loc[:,'Application']

# %% Populate Project Description Field
df['full_desc'] = (df['WorkDescription'].astype(str) + ', ' + df['ProjectName'].astype(str))
out_df['project_description'] = df.loc[:,'full_desc']

# %% Populate Permit Class Field
out_df['permit_class'] = df.loc[:,'Application_Type']

# %% Populate Permit Type Field
out_df['permit_type'] = df.loc[:,'Application_Subtype']

# %% #%% Populate Estimated Cost Field
out_df['estimated_cost'] = df['Valuation']

# %% Populate Applied Date Filed
out_df ['applied_date'] = df.loc[:,'OpenDate']

# %% Populate Issued Date Filed
out_df ['issued_date'] = df.loc[:,'ISSUED_DATE']

# %% Populate Completed Date Filed
out_df ['finaled_date'] = df.loc[:,'FINALED_DATE']

# %% Formate Date Fields
out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')
out_df['finaled_date'] = pd.to_datetime(out_df['finaled_date'], errors = 'coerce')

#%% POPULATE ADDRESS
out_df['address'] = df.loc[:,'Address']

#%% Generate Lat and Lon column from point geometry
df['lon'] = df['geometry'].x
df['lat'] = df['geometry'].y

# %% Popluate Coordinate Fields
out_df.loc[:,'latitude'] = df.loc[:,'lat']
out_df.loc[:,'longitude'] = df.loc[:,'lon']

#%% Populate Parcel Number
out_df['parcel_number']= df.loc[:,'Parcel_Number']
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
