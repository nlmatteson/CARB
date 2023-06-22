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
# corona data
test = 'city-corona-final.geojson'
#%% 
raw = gpd.read_file(root + test)

#%%
print(raw.columns.to_list())

# %% List Desired Fields

fields = ['description', 'permittype',
'applied', 'jobvalue', 'permit_no', 'finaled', 'site_streetname', 'site_city',
'issued', 'site_number', 'site_streetid', 'site_st_no',
'notes', 'permitsubtype', 'site_zip', 'site_addr',
'approved', 'site_apn', 'geometry']
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

out_df['place'] = 'Corona city'
#out_df['county_name'] =

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
out_df['zipcode'] = df['Address'].apply(extract_zipcode)'''

out_df['zipcode'] = df['site_zip']


out_df.head()

# %%  Populate Permit Number Field

out_df['permit_number'] = df.loc[:,'permit_no']
# %% Rectify Description Fields

full_description = df[[
'description', 'notes']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

#%%  Populate Permit Description Field
out_df['project_description'] = full_description

# %% Populate Permit Class Field

out_df['permit_class'] = df.loc[:,'permittype']

# %% Populate Permit Class Field

out_df['permit_type'] = df.loc[:,'permitsubtype']

#%% Populate Estimated Cost Field

out_df['estimated_cost'] = df['jobvalue']


# %% Populate Applied Date Filed

out_df ['applied_date'] = df.loc[:,'applied']

# %% Populate Issued Date Filed

out_df ['issued_date'] = df.loc[:,'issued']

# %% Populate Completed Date Feild

out_df ['finaled_date'] = df.loc[:,'finaled']

# %% Populate Address Feild

out_df['parcel_number'] = df.loc[:,'site_apn']

# %% Generate Lat and Lon column from point geometry

df['lon'] = df['geometry'].x
df['lat'] = df['geometry'].y

# %% Popluate Coordinate Fields

out_df.loc[:,'latitude'] = df.loc[:,'lat']
out_df.loc[:,'longitude'] = df.loc[:,'lon']
 
# %% Generate Full Address

df['full_address'] = (df['site_addr'].astype(str) + ', ' + df['site_city'].astype(str) + ', ' +  df['site_state'].astype(str) +', '+ df['site_unit_no'].astype(str))

# %% Populate Address Field

out_df['address'] = df.loc[:,'full_address']

# %% Populate File Name

out_df['file_name'] = test

# %% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')
out_df['finaled_date'] = pd.to_datetime(out_df['finaled_date'], errors = 'coerce')

#%% drop duplicates
print(len(out_df))
out_df = out_df.drop_duplicates()
print(len(out_df))
# %% Output to Clean CSV File

out_root = 'V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\3_permit-processing\\'
out_df.to_csv( out_root + os.path.splitext(test)[0] + '_may-update.csv')
# %%
