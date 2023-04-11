#%% imports
import pandas as pd
import geopandas as gpd
import numpy as np
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import nltk


#%% read in file

df=pd.read_csv("/Users/Nicole.lynn/Desktop/22-23 CARB GSR/CEDARS/claims_record_2018.csv")


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
ind.sum() #6185

#%% creating output file
output = df.loc[ind,:]

#%% exporting output file

output.to_csv('2018_filtered.csv')
# %%
