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
# placer county
test = 'county-placer-final.geojson'
#%% Its a geojson file
raw = gpd.read_file(root + test)

#%%
print(raw.columns.to_list())
# %%  This file is incredibly messy and there are many columns which
# can mean the same thing, just slight variations 
fields = ['ActiveBuilding_ExcelToTable_OBJ',
'ActiveBuilding_ExcelToTable_B1_',
'ActiveBuilding_ExcelToTable_Sco',
'ActiveBuilding_ExcelToTable_Pro',
'ActiveBuilding_ExcelToTable_Des',
'ActiveBuilding_ExcelToTable_APN',
'ActiveBuilding_ExcelToTable_Sta',
'ActiveBuilding_ExcelToTable_Add'
'ASSESSORS_Parcel_point_CREATED1',
'ASSESSORS_Parcel_point_GISAPN',
'ASSESSORS_Parcel_point_APN',
'ASSESSORS_Parcel_point_LAST_EDI',
'ASSESSORS_Parcel_point_LAST_E_1',
'ASSESSORS_Parcel_point_POINT_X',
'ASSESSORS_Parcel_point_POINT_Y',
'ASSESSORS_Parcel_point_PARCEL_L'
'geometry']

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
out_df['county_name'] = 'Placer County'
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
out_df['zipcode'] = df['ActiveBuilding_ExcelToTable_Add'].apply(extract_zipcode)

out_df.head()

# %%  Populate Permit Number Field

out_df['permit_number'] = df.loc[:,'ActiveBuilding_ExcelToTable_B1_']

# %% Populate Project Description Field

out_df['project_description'] = df.loc[:,'ActiveBuilding_ExcelToTable_Des']

# %% Populate Permit Type Field

out_df['permit_type'] = df.loc[:,'ActiveBuilding_ExcelToTable_Sco']

# %%
out_df['applied_date']=df.loc[:,'ASSESSORS_Parcel_point_CREATED1']
# %%  Formate Date Fields
out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')


# %% Populate Address Field

out_df['address'] = df.loc[:,'ActiveBuilding_ExcelToTable_Add']


#%% Generate Lat and Lon column from point geometry

df['lon'] = df['geometry'].x
df['lat'] = df['geometry'].y

# %% Popluate Coordinate Fields

out_df.loc[:,'latitude'] = df.loc[:,'lat']
out_df.loc[:,'longitude'] = df.loc[:,'lon']


# %% populate parcel number
out_df['parcel_number']= df.loc[:,'ASSESSORS_Parcel_point_APN']

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
