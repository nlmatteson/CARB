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
# santa barbara county
test = 'county-santa-barbara-final.csv'
raw = pd.read_csv(root + test)
print(raw.columns.to_list())

# %% List Desired Fields
fields= ['Date', 'Application Number',
'Permit Type', 'Description', 'Project Name']

#DOESN'T HAVE ADDRESS FIELD
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
    'file_name']

out_df = pd.DataFrame(index = df.index,
    columns = cols)
# %% Populate Permit Number Field
out_df['permit_number'] = df.loc[:,'Application Number']

# %% Populate permit class
out_df['permit_class'] = df.loc[:,'Permit Type']

#%% populate permit type
out_df['permit_type'] = df.loc[:,'Project Name']
# %% populate description
out_df['project_description']= df.loc[:,'Description']

# %%  Populate  Date Fieled
out_df ['applied_date'] = df.loc[:,'Date']

# %% Formate Date Fields
out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')

# %% Populate Address Feild
## This file doesn't have an address!

# %%
