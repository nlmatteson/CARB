#%% Package Imports

import pandas as pd
import numpy as np
import datetime as dt
import os

# %% Set Working Directory
#root = '../2_working-files'
root = "V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\2_working-files\\"
os.chdir(root)
files = os.listdir()

# %% Read In Raw Table
test = 'city-anaheim-final.csv'
#test = files[2]
raw = pd.read_csv(root + test)
print(raw.columns.to_list())

# %%  List Desired Fields

fields = ['Permit_Number',
'Permit_Location_Address',
'Parcel',
'Census',
'Type_of_Work',
'Permit_Scope_Description',
'Valuation', 
'Application_Received',
'Permit_Issued', 
'Permit_Finalized']

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

out_df['place'] = 'Anaheim city'
#out_df['county_name'] =

#%% populate zipcode field
import re 
# Function to extract zip code using regular expression
def extract_zipcode(address):
    zipcode = re.findall(r'\b\d{5}\b', address)
    if zipcode:
        return zipcode[0]
    else:
        return None

# Apply the function to the 'address' column and create a new 'zipcode' column
out_df['zipcode'] = df['Permit_Location_Address'].apply(extract_zipcode)


# %% Populate Permit Number Field

out_df['permit_number'] = df.loc[:,'Permit_Number']

# %% Populate Project Description Field

out_df['project_description'] = df.loc[:,'Permit_Scope_Description']

# %% Populate Permit Class Field

out_df['permit_class'] = df.loc[:,'Census']

# %% Populate Permit Class Field

out_df['permit_type'] = df.loc[:,'Type_of_Work']

#%% Populate Estimated Cost Field

out_df['estimated_cost'] = df['Valuation']

# %% Populate Applied Date Filed

out_df ['applied_date'] = df.loc[:,'Application_Received']

# %% Populate Issued Date Filed

out_df ['issued_date'] = df.loc[:,'Permit_Issued']

# %% Populate Completed Date Filed

out_df ['finaled_date'] = df.loc[:,'Permit_Finalized']

# %% Populate Address Feild

out_df['address'] = df.loc[:,'Permit_Location_Address']

# %% Populate Parcel Number

out_df.loc[:,'parcel_number'] = df.loc[:,'Parcel']

#%% Populate File Name

out_df['file_name'] = test

#%% drop duplicates
print(len(out_df))
out_df = out_df.drop_duplicates()
print(len(out_df))

# %% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')
out_df['finaled_date'] = pd.to_datetime(out_df['finaled_date'], errors = 'coerce')

# %% Output to Clean CSV File

out_root = 'V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\3_permit-processing\\'
out_df.to_csv( out_root + os.path.splitext(test)[0] + '_may-update.csv')

# %%
