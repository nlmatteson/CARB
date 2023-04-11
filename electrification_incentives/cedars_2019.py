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

df=pd.read_csv("/Users/Nicole.lynn/Desktop/22-23 CARB GSR/CEDARS/claims_record_2019.csv")

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
ind.sum() #3961

#%% creating output file
output = df.loc[ind,:]

#%% exporting output file

output.to_csv('2019_filtered.csv')

''''
# %% Old process - kept because it may be helpful to see what coloumns are important for what kind of information and 
# the process used

# select columns
# these are the fields which seemed more pertinent to our analysis
fields = ['Claim ID',
 'Year',
 'PA',
 'Program ID',
 'Program Name',
 'Program Group',
 'Primary Sector',
 'Program Sector',
 'Statewide Program',
 'Program Category',
 'Direct Install',
 'Financing',
 'Program Implementer',
 'Claim Year Quarter',
 'Delivery Type',
 'Building Type',
 'Climate Zone',
 'Measure Electric End Use Shape',
 'Target Sector',
 'Measure Application Type',
 'Measure Code',
 'Measure Description',
 'Measure Impact Type',
 'Measure ID',
 'Measure Qualifier',
 'Location Cost Adjustment',
 'Labor Rate',
 'Measure Technology ID',
 'Technology Group',
 'Technology Type',
 'Use Category',
 'Use Subcategory',
 'Pre-Existing Technology Description',
 'Standard Technology Description',
 'Source Description',
 'Normalizing Unit',
 'Number of Units',
 'Unit Direct Install Labor',
 'Unit Direct Install Materials',
 'Unit End User Rebate',
 'Unit Incentive to Others',
 'Gross Measure Cost',
 'Gross Measure Cost Early Retirement',
 'End User Rebate',
 'Incentive to Others',
 'Direct Install Labor',
 'Direct Install Materials',
 'Budget',
 'Gross Participant Cost',
 'Net Participant Cost',
 'Weighted Program Cost',
 'Weighted Admin Costs Overhead and GA']

#%% read in file

#df=pd.read_csv("/Users/Nicole.lynn/Desktop/22-23 CARB GSR/CEDARS/claims_record_2019.csv")

# all available columns:
'''['Claim ID',
 'Year',
 'PA',
 'Program ID',
 'Program Name',
 'Program Group',
 'Primary Sector',
 'Program Sector',
 'Statewide Program',
 'Program Category',
 'Direct Install',
 'Financing',
 'Program Implementer',
 'Resource Flag',
 'Non Resource Flag',
 'Deemed Flag',
 'Custom Flag',
 'Upstream Flag',
 'Midstream Flag',
 'Downstream Flag',
 'Audit Flag',
 'Exclude From Budget Flag',
 'Exclude from CE Flag',
 'Claim Year Quarter',
 'Measure Table',
 'Measure Sector',
 'Delivery Type',
 'Building Type',
 'Climate Zone',
 'Gas Savings Profile',
 'Gas Sector',
 'Measure Electric End Use Shape',
 'Target Sector',
 'Measure Application Type',
 'Measure Code',
 'Measure Description',
 'Measure Impact Type',
 'Measure ID',
 'Measure Qualifier',
 'Interactive Effect Table Name',
 'Location Cost Adjustment',
 'Labor Rate',
 'Measure Technology ID',
 'Technology Group',
 'Technology Type',
 'Use Category',
 'Use Subcategory',
 'Pre-Existing Technology Description',
 'Standard Technology Description',
 'Source Description',
 'Version',
 'Normalizing Unit',
 'Number of Units',
 'Unit kWh First Baseline',
 'Unit kW First Baseline',
 'Unit Therm First Baseline',
 'Unit kWh Second Baseline',
 'Unit kW Second Baseline',
 'Unit Therm Second Baseline',
 'Unit Gross Measure Cost First Baseline',
 'Unit Gross Measure Cost Second Baseline',
 'Unit Direct Install Labor',
 'Unit Direct Install Materials',
 'Unit End User Rebate',
 'Unit Incentive to Others',
 'NTG ID',
 'NTGR kWh',
 'NTGR kW',
 'NTGR Therm',
 'NTGR Cost',
 'EUL ID',
 'EUL Years',
 'RUL ID',
 'RUL Years',
 'GSIA ID',
 'Realization Rate kWh',
 'Realization Rate kW',
 'Realization Rate Therm',
 'Installation Rate kWh',
 'Installation Rate kW',
 'Installation Rate Therm',
 'Measure Residential Flag',
 'Measure Upstream Flag',
 'First Year Gross kWh',
 'First Year Gross kW',
 'First Year Gross Therm',
 'First Year Net kWh',
 'First Year Net kW',
 'First Year Net Therm',
 'Lifecycle Gross kWh',
 'Lifecycle Gross Therm',
 'Lifecycle Net kWh',
 'Lifecycle Net Therm',
 'Gross Measure Cost',
 'Gross Measure Cost Early Retirement',
 'End User Rebate',
 'Incentive to Others',
 'Direct Install Labor',
 'Direct Install Materials',
 'Budget',
 'Gross Participant Cost',
 'Net Participant Cost',
 'Weighted Program Cost',
 'Weighted Admin Costs Overhead and GA',
 'Weighted Admin Costs Other',
 'Weighted Marketing Outreach',
 'Weighted Direct Install Activity',
 'Weighted Direct Install Installation',
 'Weighted Direct Install Hardware and Materials',
 'Weighted Direct Install Rebate and Inspection',
 'Weighted EMV',
 'Weighted User Input Incentive',
 'Weighted Costs Recovered From Other Sources',
 'Electric Supply Cost',
 'Electric Supply Cost Gross',
 'Gas Supply Cost',
 'Gas Supply Cost Gross',
 'Other Benefits',
 'Other Benefits Gross',
 'Other Costs',
 'Other Costs Gross',
 'Total System Benefit',
 'Total System Benefit Gross',
 'TRC',
 'PAC',
 'TRC No Admin',
 'PAC No Admin',
 'RIM',
 'Benefits',
 'Electric Benefits',
 'Gas Benefits',
 'TRC Cost',
 'PAC Cost',
 'TRC Cost No Admin',
 'PAC Cost No Admin',
 'RIM Cost',
 'Levelized Benefits Electric',
 'Levelized Benefits Gas',
 'Levelized TRC Cost',
 'Levelized PAC Cost',
 'Levelized RIM Cost',
 'Levelized TRC Cost No Admin',
 'Levelized PAC Cost No Admin',
 'Levelized Net Benefits TRC Electric',
 'Levelized Net Benefits TRC Gas',
 'Levelized Net Benefits PAC Electric',
 'Levelized Net Benefits PAC Gas',
 'Levelized Net Benefits RIM Electric',
 'Levelized Net Benefits RIM Gas',
 'Levelized Net Benefits TRC No Admin Electric',
 'Levelized Net Benefits TRC No Admin Gas',
 'Levelized Net Benefits PAC No Admin Electric',
 'Levelized Net Benefits PAC No Admin Gas',
 'First Year Gross Elec CO2',
 'First Year Gross Gas CO2',
 'First Year Net Elec CO2',
 'First Year Net Gas CO2',
 'Lifecycle Gross Elec CO2',
 'Lifecycle Gross Gas CO2',
 'Lifecycle Net Elec CO2',
 'Lifecycle Net Gas CO2',
 'First Year Gross Elec NOx',
 'First Year Gross Gas NOx',
 'First Year Net Elec NOx',
 'First Year Net Gas NOx',
 'Lifecycle Gross Elec NOx',
 'Lifecycle Gross Gas NOx',
 'Lifecycle Net Elec NOx',
 'Lifecycle Net Gas NOx',
 'First Year Gross PM10',
 'First Year Net PM10',
 'Lifecycle Gross PM10',
 'Lifecycle Net PM10']'''

#%% Loading in only relavent columns
df = pd.read_csv("/Users/Nicole.lynn/Desktop/22-23 CARB GSR/CEDARS/claims_record_2019.csv",
                 usecols = fields, 
                 header = 0,
                 skiprows = [1],
                 low_memory = False)

df.reset_index(drop = True, inplace = True)

# %% #%% Extract Columns
columns = df.columns.to_list()

# %% Filtering Ideas 
# Measure Description: Contains 'Gas', 'Duct'(?) 
# ~contain [Air, Aerator, Thermostat, LED, 'Shower']
# delivery type "Downstream custom"
# Measure description
# measure impact type doesn't have fuel sub
# Technology group
# Use category

#%% checking some columns 
measure_impact = pd.Series(df['Measure Impact Type'].unique())
program_sector = pd.Series(df['Program Sector'].unique()) #can filter res and com
technology_group = pd.Series(df['Technology Group'].unique()) #not super helpful
use_category = pd.Series(df['Use Category'].unique()) # this is a good one

# %%
df['Measure Description'].sample(10)

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

#%% 

# %% Combine Index and Filter Raw Table

all_ind = [ program_sector_ind,
            use_category_ind ]
all_ind = pd.concat(all_ind, axis = 1).all(axis = 1)

cedars = df.loc[all_ind,:]

# %% Filtered a good amount out but not enough
# went from 945,780 to 649,379
# there is still measures with light fixtures and aerators for sinks etc

print(len(df))
print(len(cedars))

# %% Checking more columns

use_category = pd.Series(cedars['Use Category'].unique())
measure_descr= pd.Series(cedars['Measure Description'].unique())
pre_existing = pd.Series(cedars['Pre-Existing Technology Description'].unique())
technology_group = pd.Series(cedars['Technology Group'].unique())
building_type = pd.Series(cedars['Building Type'].unique())

#%% Filtering by technology group and building type

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

tech_filter_ind = cedars['Technology Group'].isin(tech_filter)

building_filter = ['Residential Single Family',
                   'Residential Multi-family',
                   'Residential Mobile Home',
                   'Residential',
                   'Commercial']

building_filter_ind = cedars['Building Type'].isin(building_filter)

#%% combining index and filter table

all_ind = [ tech_filter_ind,
            building_filter_ind ]

all_ind = pd.concat(all_ind, axis = 1).all(axis = 1)

cedars2 = cedars.loc[all_ind,:]

print(len(cedars2))
# 454,799
# originally 945,780 
#%% 
len(cedars2['Program ID'].unique())

#%% Only thing left to filter on is measure description

measure_descr= pd.Series(cedars2['Measure Description'].unique())

#%% 
import nltk
cedars2['Measure Description Word Count'] = cedars2['Measure Description'].apply(lambda x : nltk.FreqDist(nltk.word_tokenize(x)))

#%% 

word_count_dict = nltk.FreqDist(nltk.word_tokenize(cedars2['Measure Description'].str.cat(sep=' ')))

# %% List of key terms
# i should make the column all in lower case first so I catch everything

keys = ['wh',
        'dhw',
        'hot water',
        'heater',
        #CAS repair?,
        'gas',
        'heat pump',
        'pump',
        #washing machines?,
        'hvac',
        'gasfurnace',
        'wtrht',
        'washer',
        'dryer',
        'electric',
        #thermostat?,
        'energystar',
        'kw',
        'upgrade',
        'oven',

        ]

#%% make measure description column all lower case

cedars2['Measure Description']= cedars2['Measure Description'].str.lower()

#%% look into these things
# 2018 HEA Whole Home Savings - Operational, Behavioral
# 2019 BIG Whole Home Savings
# 2019 Franklin Energy Whole Home Savings
# MF-Home Upgrade-Total Products Rebate
# KICKER FOR 20% Improvement
# 2013 T-24 Std B100 - RA-MF Whole Building
# ESAP_MEASURE_EUL_10
# SCG Advanced Home Upgrade- SF Whole Building (IOU) Gas Only
