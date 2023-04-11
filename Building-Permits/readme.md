# This folder holds the python files that I used to manipulate the building permit data into the format we need for the PostGis database
Each municipality's building permit data had different columns, data types and format. I had to go through each individual file to extract the data that we needed and generate a new dataframe with a consistent format.

####The cleaned files that are ready for PostGis are all .csv files and have the following structure:

cols = [

'permit_number',  #the individual permit’s unique identifier given by the municipality (str)

'project_description', #the description of the permit, contains details of what work was done. This will likely include specifics about amperage, panel size, what prompted the upgrade, if relocation was necessary, etc. (str)

'permit_class', # general classification of the type of permit (str)

'permit_type', # more precise classification to the type of permit (str)

'estimated_cost', # estimated cost of the project (int)

'applied_date', #date of when customer applied for the permit (datetime)

'issued_date', # date of when the permit was issued (datetime)

'finaled_date', # date of when the permit has finished all required inspections and is complete (date time)

'address', # address of the permit.  (text)

'parcel_number', # the APN of the parcel (text)

'latitude', #latitute of the parcel. Will need to create geometry of lat and lon columns EPSG 3310

'longitude', # longitude of parcel

'file_name' #the original file name where the table came from]
