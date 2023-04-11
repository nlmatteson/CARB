#%% imports
import pandas as pd
import geopandas as gpd
import numpy as np
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import nltk

# %% read in file
# this is the file we used to get the key terms to filter the earlier year's data
# this file is already filtered for fuel substitution so our thinking is we can match key terms used to describe the measure 
# to filter the other year's data

df = pd.read_excel('/Users/Nicole.lynn/Desktop/22-23 CARB GSR/CEDARS/Fuel Sub 2020 Claims_3.10.xls')
# %% cleaning up the measure description column
df['Measure Description']= df['Measure Description'].str.lower()
df['Measure Description'] = df['Measure Description'].str.replace('-',' ')
df['Measure Description'] = df['Measure Description'].str.replace('_',' ')


# %% creating dictionary of key terms

word_count_dict = nltk.FreqDist(nltk.word_tokenize(df['Measure Description'].str.cat(sep=' '))) 

# %% creating a dataframe from the dictionary of key terms

word_count_df = pd.DataFrame.from_dict(word_count_dict, orient='index').sort_values(by=0, ascending=False)
#%% These are the most common terms 
minisplit  = df['Measure Description'].str.contains('mini split', case = False)

dxhp  = df['Measure Description'].str.contains('dxhp', case = False)

heatpump = df['Measure Description'].str.contains('heat pump', case= False)

#%% creating index
ind = (minisplit) | (dxhp) | (heatpump)
# %% getting sum
ind.sum() #5523
# %% creating output file
output = df.loc[ind,:]

#%% exporting output file
output.to_csv('2020_filtered.csv')
# %%
