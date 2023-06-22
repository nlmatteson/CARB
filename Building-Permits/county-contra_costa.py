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
# contra costa county
test = 'county-contra_costa-final.csv'
raw = pd.read_csv(root + test)
print(raw.columns.to_list())

# %% List Desired Fields
fields= ['File Date', 'Record Number',
'Related Records', 'Record Type', 'Description', 'Address']

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
out_df['county_name'] = 'Contra Costa County'
#%% populate zipcode field

#the zipcodes in this df are longer than 5 digits so I am only keeping the first 5
# which looks right

# Function to extract first five digits of number starting with 9
def extract_zip(address):
    if isinstance(address, str):
        numbers = address.split()  # Split address by whitespace
        for number in numbers:
            if number.startswith('9'):
                return number[:5]  # Keep first five digits
    return None


# Convert 'Address' column to string
df['Address'] = df['Address'].astype(str)

# Apply the function to the 'address' column and create a new 'zipcode' column
out_df['zipcode'] = df['Address'].apply(extract_zip)

out_df.head()

# %% Populate Permit Number Field
out_df['permit_number'] = df.loc[:,'Record Number']

# %% Populate permit type

out_df['permit_type'] = df.loc[:,'Record Type']

# %% populate description
out_df['project_description']= df.loc[:,'Description']

# %%  Populate  Date Fieled

out_df ['applied_date'] = df.loc[:,'File Date']

# %% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')

# %% Populate Address Feild

out_df['address'] = df.loc[:,'Address']

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
