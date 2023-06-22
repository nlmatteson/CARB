#%% Package Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import datetime as dt
import os

#%% Set Working Directory
root = "V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\2_working-files\\"
#root = '..\2_working-files'
os.chdir(root)
files = os.listdir()

#%% Read Raw Table
# san fransisco
test = 'city_county-san_fran-final.geojson'
raw = gpd.read_file(os.path.join(root, test))

#%%
print(raw.columns.to_list())

# %% List Desired Fields
# this file has both a permit number and record id number, and they are different

fields = ['record_id', 'proposed_construction_type_description',
'issued_date', 'existing_construction_type_description', 'zipcode',
'description', 'permit_creation_date', 'filed_date', 'street_name', 'block', 'estimated_cost', 'permit_expiration_date', 'unit_suffix', 'proposed_construction_type', 'permit_type_definition', 'status',
'completed_date', 'permit_number', 'street_number_suffix',
'street_suffix', 'unit', 'permit_type','street_number', 'structural_notification',
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

out_df['place'] = 'San Francisco city'
out_df['county_name'] = 'San Francisco County'

#%% populate zipcode field

out_df['zipcode'] = df['zipcode']
# %%  Populate Permit Number Field

out_df['permit_number'] = df.loc[:,'record_id']

# %% Populate Project Description Field

out_df['project_description'] = df.loc[:,'description']

# %% Populate Permit Class Field

out_df['permit_class'] = df.loc[:,'proposed_construction_type_description']

# %% Populate Permit Type Field

out_df['permit_type'] = df.loc[:,'permit_type_definition']

# %% #%% Populate Estimated Cost Field

out_df['estimated_cost'] = df['revised_cost']

# %% Populate Applied Date Filed

out_df ['applied_date'] = df.loc[:,'permit_creation_date']

# %% Populate Issued Date Filed

out_df ['issued_date'] = df.loc[:,'issued_date']

# %% Populate Completed Date Filed

out_df ['finaled_date'] = df.loc[:,'completed_date']


# %% Generate Full Address

df['full_address'] = (df['street_number'].astype(str) + ' ' + df['street_name'].astype(str) + ' ' +  df['street_suffix'].astype(str) +', '+ df['unit'].astype(str) + ', ' + df['zipcode'].astype(str))

# %% Populate Address Field

out_df['address'] = df.loc[:,'full_address']


#%% Generate Lat and Lon column from point geometry

df['lon'] = df['geometry'].x
df['lat'] = df['geometry'].y

# %% Popluate Coordinate Fields

out_df.loc[:,'latitude'] = df.loc[:,'lat']
out_df.loc[:,'longitude'] = df.loc[:,'lon']


#%% Populate File Name

out_df['file_name'] = test

# %% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')
out_df['finaled_date'] = pd.to_datetime(out_df['finaled_date'], errors = 'coerce')


#%% drop duplicates
print(len(out_df))
out_df=out_df.drop_duplicates()
print(len(out_df))
#%% Output to Clean CSV File

out_root = 'V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\3_permit-processing\\'
#out_root = '../3_permit-processing'
out_df.to_csv( out_root + os.path.splitext(test)[0] + '_may-update.csv')
#out_df.to_csv(os.path.join(out_root, os.path.splitext(basename(path))[0] + '_clean.csv'))

#file_name = os.path.basename(path)
#base_name = os.path.splitext(file_name)[0]
#out_df.to_csv(os.path.join(out_root, base_name + '_clean.csv')

'''# %% Output to Clean CSV File

out_root = 'V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\Permit_Processing\\'
out_df.to_csv( out_root + os.path.splitext(test)[0] + '_may-update.csv')'''
# %%
