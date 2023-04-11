#%% imports
import pandas as pd
import geopandas as gpd
import numpy as np
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import nltk


#%% read in file
# https://cedars.sound-data.com/reports/record-level/

df=pd.read_csv("/Users/Nicole.lynn/Desktop/22-23 CARB GSR/CEDARS/claims_record_2016.csv")

#OUR PROCESS
# For all records before 2020, there is no "Fuel Sub" category in the "Measure Impact Type" column
# we want to filter down the measures to only include measures related to fuel substitution
# our process is to use the words most common in the measure description column as keys to match on for measures we KNOW are fuel substitution (from 2020, 2021 data)

# %% cleaning up the strings in Measure Description column
# making all letters lower case
df['Measure Description']= df['Measure Description'].str.lower()

# replacing "-"
df['Measure Description'] = df['Measure Description'].str.replace('-',' ')

# replacing "_"
df['Measure Description'] = df['Measure Description'].str.replace('_',' ')

# %% getting dictionary of the most frequent words found in the Measure Description column
word_count_dict = nltk.FreqDist(nltk.word_tokenize(df['Measure Description'].str.cat(sep=' '))) 

# %% turning the dictionary into a dataframe and sorting values
word_count_df = pd.DataFrame.from_dict(word_count_dict, orient='index').sort_values(by=0, ascending=False)

#%% chosing key terms
# these words were selected as the most common phrases in the measure description columns for measures WE KNOW are related to fuel substitution
minisplit  = df['Measure Description'].str.contains('mini split', case = False)

dxhp  = df['Measure Description'].str.contains('dxhp', case = False)

heatpump = df['Measure Description'].str.contains('heat pump', case= False)

#%% making index for keys

ind = (minisplit) | (dxhp) | (heatpump)

# %% checking sum 
ind.sum() #8579

#%% creating output file
output = df.loc[ind,:]

#%% exporting output file

output.to_csv('2016_filtered.csv')





# %% old code with process which filtered down claims by individual column values
'''
df = pd.read_csv("/Users/Nicole.lynn/Desktop/22-23 CARB GSR/CEDARS/claims_record_2016.csv",
                 usecols = fields, 
                 header = 0,
                 skiprows = [1],
                 low_memory = False)

df.reset_index(drop = True, inplace = True)

# %% Extract Columns
columns = df.columns.to_list()

#%% checking some columns 

program_sector = pd.Series(df['Program Sector'].unique()) #can filter res and com
technology_group = pd.Series(df['Technology Group'].unique()) 
use_category = pd.Series(df['Use Category'].unique()) # this is a good one
measure_descr= pd.Series(df['Measure Description'].unique())
pre_existing = pd.Series(df['Pre-Existing Technology Description'].unique())



#%% Construct Filters and Associated Indexes

program_sector_filter = [ 'Res', 'Com']
program_sector_ind = df['Program Sector'].isin(program_sector_filter)

use_category_filter = ['Whole Building',
                       'Appliance or Plug Load',
                       'Service and Domestic Hot Water',
                       'HVAC',
                       'Service',
                       'Process Heat',
                       'Food Service',
                       'Non-Savings Meaure']

use_category_ind = df['Use Category'].isin(use_category_filter)

tech_filter = [ 'Whole Building',
               'Plumbing Fixture',
               'HVAC Technology',
               'Space Heating Equipment',
               'HVAC Air Distribution',
               'dx HP Equipment',
               'dx AC Equipment',
               'Water Heating Equipment',
               'Cooking Equipment',
               'Pump System',
               'Food Service']

tech_filter_ind = df['Technology Group'].isin(tech_filter)

building_filter = ['Residential Single Family',
                   'Residential Multi-family',
                   'Residential Mobile Home',
                   'Residential',
                   'Commercial']

building_filter_ind = df['Building Type'].isin(building_filter)


# %% Combine Index and Filter Raw Table

all_ind = [ program_sector_ind,
            use_category_ind,
            tech_filter_ind,
            building_filter_ind]
all_ind = pd.concat(all_ind, axis = 1).all(axis = 1)

cedars = df.loc[all_ind,:]

# %% Checking how many we filtered out

print(len(df)) #1,332,346
print(len(cedars)) #367,227

# %%
program_name = pd.Series(cedars['Program Name'].unique())
# %%
cedars.PA.value_counts()
# %%
cedars['Program ID'].value_counts()
# %%
cedars['Climate Zone'].value_counts()
# %%'''
