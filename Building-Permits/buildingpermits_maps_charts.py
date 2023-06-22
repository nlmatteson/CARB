# %%
import pandas as pd
import geopandas as gpd
import os
import seaborn as sns
sns.set_theme(style="whitegrid")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import contextily as ctx

# %%
# Loading the Justice 40 dataset. Source: https://screeningtool.geoplatform.gov/en/#3/33.47/-97.5
j40 = gpd.read_file('usa.shp')

# %%
# Only keep California Data
j40= j40.loc[j40['SF'] == 'California']

# %%
# Loading California City and County Boundaries. Source: https://gis.data.ca.gov/datasets/CDTFA::boe-cityanx2022-final-1/explore?location=36.521027%2C-119.832751%2C7.04
cities_counties = gpd.read_file('City_and_County_Boundary_Line_Changes.geojson')

# %%
# Checking dataset columns
cities_counties.columns

# %%
# Step 1 of only keeping necessary columns
cols_to_keep1 = ['COUNTY', 'CITY','last_edited_date','geometry']

# %%
# Creating dataset with only the necessary columns
cities_counties_clean = cities_counties.loc[:, cols_to_keep1]

# %%
# Creating list of the names of all the cities we have data for
city_names = ['Alameda','Anaheim','Antioch','Ceres','Chula Vista','Corona','San Fransisco','Fairfield','Hanford',
'Los Angeles','Los Gatos','Oakland','Oceanside','Ojai','Pasadena','Pleasanton','Rancho Cucamonga','Redding','Richmond','Riverside',
'Roseville','San Diego','San Jose','San Mateo','San Rafael','Santa Monica','Santa Rosa','Victorville', 'West Sacramento',
'Yorba Linda','Yuba', 'San Francisco', 'Garden Grove', 'Santa Clara', 'Clovis','Paso Robles']

# %%
# Creating list of the names of all the counties we have data for
county_names = ['Contra Costa County','El Dorado County','Humboldt County','Kern County','Lake County',
'Marin County','Nevada County','Placer County','Riverside County','Sacramento County','San Bernardino County',
'San Diego County', 'San Mateo County','Santa Barbara County','Solano County','Stanislaus County','Tulare County',
'Yolo County','San Francisco County', 'Los Angeles County']

# %%
# Creating dataframe of all the cities we have data for with associated geometry
cities_new = cities_counties_clean.loc[cities_counties_clean['CITY'].isin(city_names)]

# %%
# Step 1 of creating dataframe of all the counties we have data for
# The counties are distinguished by the City field equaling "Unincorporated"
counties_clean = cities_counties_clean.loc[cities_counties_clean['CITY'] == 'Unincorporated']

# %%
# Step 2 to create data frame that only has the counties we have data for
counties_new = counties_clean.loc[counties_clean['COUNTY'].isin(county_names)]

# %%
# Getting shape of counties dataset
print(counties_new.shape)

# %%
# Checking shape of cities dataset
print(cities_new.shape)

# %%
# Rough plot to see if it looks right
counties_new.plot(figsize=(10,10))

# %%
# Rough plot to see if the Cities look right
cities_new.plot(figsize=(10,10))

# %%
# Concatting the two datasets so they are all in one dataset
joined_cities_counties = pd.concat([cities_new, counties_new])

# %%
# Rough plot to check eye test
joined_cities_counties.plot()

# %%
# Getting shape of joined dataset to check if it was successful
print(joined_cities_counties.shape)

# %%
# Creating a unary union so that the cities and counties form one geometry. Then we can
# determine if a given census tract is in our sample or not
ci_union = joined_cities_counties.unary_union

# %%
# Creating a copy of the j40 dataset to get the centroids of the census tracts
focus_j40= j40.copy()


# %%
# Change dtype from object to numeric and force the errors
#if number starts with 0 it is not actually a number dtype
focus_j40['GEOID10'] = pd.to_numeric(focus_j40['GEOID10'], errors = 'coerce')

# %%
# Setting index for ease of use
focus_j40= focus_j40.set_index('GEOID10')

# %%
# Creating geoseries of census tract centroids
j40_centroids = focus_j40.geometry.centroid

# %%
# Checking if it was successful
j40_centroids

# %%
#Need to turn the geoseries into a geodataframe
#Naming the series
j40_centroids.name = 'j40_centroids'
#creating envelope
env = j40_centroids.envelope
#Creating gdf with envelope and setting the crs
j40_centroids_gdf= gpd.GeoDataFrame(geometry=gpd.GeoSeries(env), crs='4326')
#renaming column to get geometry column set
j40_centroids_gdf = j40_centroids_gdf.rename(columns={1:'geometry'}).set_geometry('geometry')

# %%
# Checking if table looks right
j40_centroids_gdf.head()

# %%
# Creating a new justice 40 dataset with the centroids of the census tracts
# instead of the polygons. Need to drop original geometry column first for the join
final_j40_centroids_gdf = focus_j40.drop(columns='geometry').join(j40_centroids_gdf)

# %%
# Creating a new boolean column in the original justice 40 dataset that states whether
# a census tract is in our data sample or not 
focus_j40["in_sample"] = final_j40_centroids_gdf.within(ci_union)

# %%
# Checking the value counts
focus_j40.in_sample.value_counts()

# %%
# Rough plot to check if this looks similar to other plot of the cities and counties that
# we have data for
focus_j40[(focus_j40.in_sample == True)].plot(figsize=(10,10), linewidth= 0.1,)

# %%
# Comparing to above map. It looks correct!
joined_cities_counties.plot(figsize=(10,10))

# %%
# Making list of necessary coloumns
cols_to_keep = ['CF',
 'EBF_PFS',
 'LMI_PFS',
 'P100_PFS',
 'LPF_PFS',
 'in_sample',
 'geometry']

# %%
# Creating final clean dataset
focus_j40_final = focus_j40.loc[:, cols_to_keep]

# %%
# Resetting index so that I can rename GEOID10 
focus_j40_final = focus_j40_final.reset_index()

# %%
# Renaming the columns to something easier to comprehend
focus_j40_final= focus_j40_final.rename(columns={'GEOID10': 'geoid', 'EBF_PFS':'Energy Burden Percentile',
'LMI_PFS': 'MHI as a percent of area median income',
'P100_PFS': 'Pct individuals < 100pct Federal Poverty Line',
'LPF_PFS': 'Pct pre-1960s housing'})

# %%
# Loading the AB 1550 data
# source: https://webmaps.arb.ca.gov/PriorityPopulations/
PP = gpd.read_file('a0000000b.gdbtable')
PP.head()


#%%
PP['Priority Population']= np.where(PP['Nondesignated']=='No', 'yes','no')

#%% 
PP.sample(15)

#%% Test Plot of PP Census Tracts

PP_wm = PP.to_crs(epsg=3857)

fig, ax = plt.subplots(1,1,figsize=(12,12))

PP_wm[PP_wm['Priority Population']== 'yes'].plot(ax=ax)


#%% Plot of Non PP census Tracts

fig, ax = plt.subplots(1,1,figsize=(12,12))

PP_wm[PP_wm['Priority Population']== 'no'].plot(ax=ax)

#%% Creating clean dataset with only Priority Pops

PP_only = PP.copy()

PP_only = PP_only.loc[PP_only['Priority Population']== 'yes']

PP_only.plot()


# %%
# Renaming the Tract column to geoid so it matches the other dataset
PP_only= PP_only.rename(columns={'Centract':'geoid'})

#%% Changing geoid data type to match focus_j40_final dtype

PP_only['geoid'] = PP_only['geoid'].astype('int64')

# %%
#create new column and set values to False. Will change later
focus_j40_final['Priority Population'] = False

# %%
#Create series of the geoid column
pp_geoid = PP_only['geoid']

# %%
#If focus_j40_final geoid is in dac_geoid, then column changes to True
focus_j40_final.loc[focus_j40_final['geoid'].isin(pp_geoid), 'Priority Population'] = True

# %%
# Checking value counts
focus_j40_final['Priority Population'].value_counts()

# %%
# Creat function that will be used to create a column that categorizes the census tracts on if they
# are an SB 535 DAC in our sample or not, or if they are a Non DAC census tract and in our sample or not

def check_df(df):
    if (df['in_sample'] == True and df['Priority Population'] == True):
        return "Priority Population in Sample"
    elif (df['in_sample'] == False and df['Priority Population'] == True):
        return "Priority Population out of Sample"
    elif (df['in_sample'] == True and df['Priority Population'] == False):
        return "Non Priority Population in Sample"
    elif (df['in_sample'] == False and df['Priority Population'] == False):
        return "Non Priority Population out of Sample"
    else: 
        return np.Nan

# %%
#apply function to df creating new column. Axis=1 for columns
focus_j40_final['Category']= focus_j40_final.apply(check_df, axis=1)

# %%
#checking if there are any NA to test if function worked
focus_j40_final['Category'].isna().sum()

# %%
# Getting value counts
focus_j40_final.Category.value_counts()

# %%
# Creating a box and whisker plot to compare across groups
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=focus_j40_final['Pct pre-1960s housing'],
                 x=focus_j40_final['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Percent of <1960 Housing', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Percent of Housing Built \n Before 1960', fontsize= 'x-large')

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=focus_j40_final['Energy Burden Percentile'],
                 x=focus_j40_final['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Energy Burden Percentile', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Energy Burden Percentile', fontsize='xx-large')

# %%
# Reprojecting to web mercator
focus_j40_wb= focus_j40_final.to_crs(epsg=3857)

# %%
# Creating map of where the different categories are in California
# The design and color palet of this map was improved by using QGIS.

fig, ax = plt.subplots(1,1,figsize=(12,12))

focus_j40_wb.plot('Category', ax=ax, legend=True,
linewidth= 0.1,
edgecolor='white',
cmap='Set2')

ax.axis('off')
ctx.add_basemap(ax,url=ctx.providers.CartoDB.Voyager)

# %%
# Setting index to geoid for ease of use
focus_j40_final= focus_j40_final.set_index('geoid')

# %%
# Loading Calenviroscreen data
# Source: https://oehha.ca.gov/calenviroscreen/report/calenviroscreen-40
ca_enviro = gpd.read_file('calenviroscreen40shpf2021shp/CES4 Final Shapefile.shp')

# %%
# Creating list of necessary columns
cols_to_keep2 = ['Tract','TotPop19', 'CIscore', 'CIscoreP','EducatP', 'Ling_IsolP','PovertyP',
'UnemplP', 'HousBurdP', 'PopCharSc','Hispanic', 'White', 'AfricanAm', 'NativeAm', 'OtherMult']

# %%
# Creating clean dataset of calenviroscreen data with only necessary columns and renaming columns
clean_ca = ca_enviro.loc[:, cols_to_keep2]
clean_ca = clean_ca.rename(columns={'Tract':'geoid','TotPop19':'Total Pop'})

# %%
# Setting index to geoid
clean_ca = clean_ca.set_index('geoid')

# %%
print('focus_j40_final before join: {}'.format(len(focus_j40)))

# %%
print('clean_ca before join: {}'.format(len(clean_ca)))

# %%
# Joining the datasets 
newdf = focus_j40_final.join(clean_ca)

# %%
# Checking if join was successful
print('new_df length: {}'.format(len(newdf)))

# %%
# Importing California Building Climate Zones
# Source: https://gis.data.ca.gov/datasets/549017ee96e341d2bbb3dd0c291a9112_0/explore?location=37.113692%2C-118.879698%2C6.81
climates= gpd.read_file('Building_Climate_Zones.geojson')

# %%
# Reprojecting to web mercator
climates_wm= climates.to_crs(epsg=3857)

# %%
fig, ax = plt.subplots(1,1,figsize=(12,12))

climates_wm.plot('BZone', ax=ax, legend=True,
linewidth= 0.1,
edgecolor='white')

ax.axis('off')
ctx.add_basemap(ax,url=ctx.providers.CartoDB.Voyager)
ax.set_title('California Building Climate Zones', fontsize='xx-large')

# %%
# Step 1 of linking census tracts to their respective bulding climate zone
# getting the centroids of the Tract polygons
centroids = newdf.geometry.centroid

# %%
#Need to turn the geoseries into a geodataframe
#Naming the series
centroids.name = 'centroids'
#creating envelope
env = centroids.envelope
#Creating gdf with envelope and setting the crs
centroids_gdf= gpd.GeoDataFrame(geometry=gpd.GeoSeries(env), crs='4326')
#renaming column to get geometry column set
centroids_gdf = centroids_gdf.rename(columns={1:'geometry'}).set_geometry('geometry')



# %%
#joining centroids and climates so we get which centroids are within the climates polygons
point_climates = gpd.sjoin(centroids_gdf, climates, how = 'left', op='within')

# %%
#setting crs
point_climates.crs = 'epsg:4326'

# %%
# Dropping unnecessary columns
point_climates= point_climates.drop(columns=['index_right','OBJECTID', 'BAcerage'])

# %%
print('new_df length before join with climate zones: {}'.format(len(newdf)))

# %%
print('points_climates length before join: {}'.format(len(point_climates)))

# %%
# Joining back to newdf but dropping geometry.
newdf_final = newdf.join(point_climates.drop(columns='geometry'))

# %%
print('newdf_final length after join: {}'.format(len(newdf_final)))

# %%
# Checking how many census tracts are within each building climate zone
newdf_final.BZone.value_counts()

# %%
newdf_final.groupby('Category')[['Hispanic', 'White', 'AfricanAm']].agg(['mean','median'])

# %%
newdf_final.groupby('Category')['Total Pop'].agg([np.sum])

# %%
# Need to make sure there are no -999 numbers in these coloumns in order to do our analyses
columns= ['Total Pop', 'CIscore', 'CIscoreP', 'EducatP', 'Ling_IsolP', 'PovertyP',
       'UnemplP', 'HousBurdP', 'PopCharSc', 'Hispanic', 'White', 'AfricanAm',
       'NativeAm', 'OtherMult']

# %%
ind = newdf_final.loc[:,columns] < 0
ind.shape

# %%
newdf_final.loc[:,columns] = newdf_final.loc[:,columns].replace(-999, np.nan)

# %%
newdf_final.isna().sum(axis =0)

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=newdf_final['White'],
                 x=newdf_final['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Percent', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Percent White', fontsize='xx-large')

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=newdf_final['Hispanic'],
                 x=newdf_final['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Percent', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Percent Hispanic', fontsize='xx-large')

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=newdf_final['AfricanAm'],
                 x=newdf_final['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Percent', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Percent African American', fontsize='xx-large')

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=newdf_final['UnemplP'],
                 x=newdf_final['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Percent', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Unemployment', fontsize='xx-large')

# %%
# Getting the total population and average Calenviroscreen Score for each of our categories
total_pops = newdf_final.groupby('Category')['Total Pop'].agg('sum')
avg_CIScore = newdf_final.groupby('Category')['CIscore'].agg('mean')


# %%
# Getting the total number of tracts in each category
total_tracts = newdf_final.groupby('Category').size()

# %%
# Getting the total number of tracts in each building climate zone
total_tractsBzone = newdf_final.groupby(['BZone']).size()

# %%
total_tractsBzone

# %%
total_tracts

# %%
avg_CIScore

# %%
total_pops


# %%
fig, ax = plt.subplots(figsize=(16,10))
ax = sns.countplot(x=newdf_final['BZone'],
                 palette="Set3",
                 order=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],
                 hue= newdf_final['Category'])

ax.set_ylabel('Count', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Count of Tracts by Building Climate Zone', fontsize='xx-large')
ax.legend(title='Category', fontsize='large', title_fontsize= 'x-large')

# %%
fig, ax = plt.subplots(figsize=(16,10))
ax = sns.countplot(x=newdf_final['BZone'],
                 palette="Set3",
                 order=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],
                 hue= newdf_final['in_sample'])

ax.set_ylabel('Count', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Count of Tracts by Building Climate Zone', fontsize='xx-large')
ax.legend(title='In Sample', fontsize='large', title_fontsize= 'large', labels=['No', 'Yes'])

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=newdf_final['PovertyP'],
                 x=newdf_final['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Percent', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Percent of Population Experiencing Poverty', fontsize='xx-large')

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=newdf_final['CIscoreP'],
                 x=newdf_final['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Percentile', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('CES 4.0 Percentile', fontsize='xx-large')

# %%
# Loading 2020 median income inflations adjusted census data
# Source: https://data.census.gov/cedsci/table?q=median%20income&g=0400000US06,06%241400000&d=ACS%205-Year%20Estimates%20Subject%20Tables&tid=ACSST5Y2020.S1903
med_income=pd.read_csv('ACSST5Y2020.S1903-Data.csv')


# %%
# Renaming columns
med_income=med_income.rename(columns={'S1903_C03_001E':'Household Med Income',
'S1903_C03_002E':'Med Income: White',
'S1903_C03_003E':'Med Income: African American',
'S1903_C03_009E': 'Med Income: Hispanic',
'S1903_C03_015E':'Med Income: Families',
'GEO_ID':'geoid'})

# %%
cols_to_keep4 = ['Household Med Income', 'Med Income: White', 'Med Income: African American',
'Med Income: Hispanic', 'Med Income: Families', 'geoid']

# %%
# Creating cleaned dataset with only necessary columns
clean_med_income =  med_income.loc[:, cols_to_keep4]


# %%
# Dropping first row
clean_med_income= clean_med_income.drop([0])

# %%
# Changing the geoid format to match the other dataset's
clean_med_income['geoid']= clean_med_income['geoid'].astype(str).str.replace('1400000US','')

# %%
# Forcing geoid to numeric
clean_med_income['geoid'] = pd.to_numeric(clean_med_income['geoid'], errors = 'coerce')
clean_med_income.info()

# %%
# Setting geoid as index to complete join
clean_med_income = clean_med_income.set_index('geoid')


# %%
# Forcing med income groups to numeric 
clean_med_income['Med Income: Hispanic'] = pd.to_numeric(clean_med_income['Med Income: Hispanic'], errors= 'coerce')
clean_med_income['Med Income: White'] = pd.to_numeric(clean_med_income['Med Income: White'], errors= 'coerce')
clean_med_income['Med Income: African American'] = pd.to_numeric(clean_med_income['Med Income: African American'], errors= 'coerce')
clean_med_income['Med Income: Families'] = pd.to_numeric(clean_med_income['Med Income: Families'], errors= 'coerce')
clean_med_income['Household Med Income'] = pd.to_numeric(clean_med_income['Household Med Income'], errors= 'coerce')

# %%
print('Length of newdf_final before join : {}'.format(len(newdf)))

# %%
print('Length of clean_med_income before join : {}'.format(len(clean_med_income)))

# %%
# Joining datasets
final_df_updated= newdf_final.join(clean_med_income)

# %%
print('Length of final_df_updated after join : {}'.format(len(final_df_updated)))

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=final_df_updated['Med Income: White'],
                 x=final_df_updated['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Median Income (dollars)', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Median Household Income for White Households', fontsize='xx-large')

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=final_df_updated['Household Med Income'],
                 x=final_df_updated['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Median Income (dollars)', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Median Household Income', fontsize='xx-large')

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=final_df_updated['Med Income: Hispanic'],
                 x=final_df_updated['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Median Income (dollars)', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Median Household Income for Hispanic Households', fontsize='xx-large')

# %%
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.boxplot(y=final_df_updated['Med Income: African American'],
                 x=final_df_updated['Category'],
                 palette="Set3",
                 order= ['Non Priority Population out of Sample','Non Priority Population in Sample','Priority Population out of Sample','Priority Population in Sample'])

ax.set_ylabel('Median Income (dollars)', fontsize= 'large')
ax.set_xlabel('')
ax.set_title('Median Household Income for African American Households', fontsize='xx-large')

# %%

final_df_updated.to_file("buildingpermitmap.geojson", driver='GeoJSON')


# %%
