# %% 
import pandas as pd
import os
import glob, os

import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

# %%
os.chdir('V:\\PIER_Data\\Nicole_Matteson\\Building_Permit_Data\\CSV')
parent_dir = r'V:\PIER_Data\Nicole_Matteson\Building_Permit_Data\CSV'
for csv_file in glob.glob(os.path.join(parent_dir, '*.csv')):
    print (csv_file)
# %%
results = [os.path.basename(f) for f in glob.glob(os.path.join(parent_dir, '*.csv'))]
# %%
print(results)
# %%
stockton_files = [f for f in results if f.startswith('city_stockton')]
# %%
cit_stockton_final = pd.concat(map(pd.read_csv, stockton_files))
# %%
cit_stockton_final.to_csv('city_stockton_final.csv')
# %%
