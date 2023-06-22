#%% Package Imports

import pandas as pd
import numpy as np
import datetime as dt
import os

#%% Set Working Directory
root = "V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\2_working-files\\"
#root = '..\2_working-files'
os.chdir(root)
files = os.listdir()

#%% Read Raw Table

test = 'city-alameda-final.csv'
raw = pd.read_csv(os.path.join(root, test))

#path = '../2_working-files/city-alamed-final.csv'
#raw = pd.read_csv(path)

print(raw.columns.to_list())

#%% List Desired Fields

fields = [
    'PermitNum',
    'Description',
    'AppliedDate',
    'IssuedDate',
    'CompletedDate',
    'OriginalAddress1',
    'OriginalAddress2',
    'OriginalCity',
    'OriginalState',
    'OriginalZip',
    'PermitClass',
    'PermitClassMapped',
    'StatusCurrent',
    'StatusCurrentMapped',
    'WorkClass',
    'WorkClassMapped',
    'PermitType',
    'PermitTypeMapped',
    'Latitude',
    'Longitude',
    'EstProjectCostDEC',
    'PIN',
    'EstProjectCost',
    'Date',
    'Permit Number',
    'Permit Type',
    'Address']

#%% Extract File for Testing

df = pd.read_csv(root + test, 
    usecols = fields, 
    header = 0,
    skiprows = [1],
    low_memory = False)

df.reset_index(drop = True, inplace = True)

#%% Create Output Dataframe Structure

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

#%% Rectify Composite Permit Number Field

out_df['permit_number'] = df['PermitNum'].fillna(df['Permit Number'])

#%% Populate Project Description Field

out_df['project_description'] = df.loc[:,'Description']

#%% Populate Permit Class Field

out_df['permit_class'] = df.loc[:,'PermitClassMapped']

#%% Rectify Composite Permit Type Field

out_df['permit_type'] = df['PermitTypeMapped'].fillna(df['Permit Type'])

#%% Populate Estimated Cost Field

out_df['estimated_cost'] = df['EstProjectCost']

#%% Populate Applied Date Filed

out_df ['applied_date'] = df.loc[:,'AppliedDate']


#%% Populate Issued Date Field

out_df['issued_date'] = df.loc[:,'IssuedDate']

#%% Rectify Composite Completed Date Field

out_df['finaled_date'] = df['CompletedDate'].fillna(df['Date'])

#%% Rectify Composite Address Fields

full_address_A = df[[
    'OriginalAddress1',
    'OriginalCity',
    'OriginalState',
    'OriginalZip']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

full_address_A[full_address_A.str.contains('nan')] = np.nan
full_address_B = df['Address']

out_df['address'] = full_address_A.fillna(full_address_B, inplace = False)

#%% Populate Parcel Number Fields

out_df.loc[:,'parcel_number'] = df.loc[:,'PIN']

#%% Populate Coordinate Fields

out_df.loc[:,'latitude'] = df.loc[:,'Latitude']
out_df.loc[:,'longitude'] = df.loc[:,'Longitude']

#%% Populate File Name

out_df['file_name'] = test

#%% Formate Date Fields

out_df['applied_date'] = pd.to_datetime(out_df['applied_date'], errors = 'coerce')
out_df['issued_date'] = pd.to_datetime(out_df['issued_date'], errors = 'coerce')
out_df['finaled_date'] = pd.to_datetime(out_df['finaled_date'], errors = 'coerce')

#%% Format city or county fields

out_df['place'] = 'Alameda city'
#out_df['county_name'] =

#%% populate zipcode field

out_df['zipcode'] = df['OriginalZip']


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

# %%
