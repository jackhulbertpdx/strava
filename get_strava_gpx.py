import gpx_converter
from gpx_converter import Converter
import re
import os
import pandas as pd
import fnmatch
import os



# Strava requires you to manually download GPX files from your account, therefore we need to define an input and output directory 

# Files where GPX files live (1 file per activity)
inpath = '/Users/jackhulbert/Desktop/Data Science Projects/Strava/export_61962341/activities'
# Where we are going to write our CSV Files
outpath = '/Users/jackhulbert/Desktop/Data Science Projects/Strava/Data/GPX Files'

#Extract GPX files from input directory and convert to pandas dataframe. We will write 1 file per activity.
def get_gpx():
	for file in os.listdir(inpath):
		#File must be GPX
	    if fnmatch.fnmatch(file,'*gpx'):
	        df = Converter(input_file=(inpath+'/'+file)).gpx_to_dataframe()
	        #Append name of file to dataframe, as this will be our join key with other strava datasets. (Activity ID = ID)
	        df['id'] = file
	        #Rename file to not contain the last 4 characters from the original filename (.gpx)
	        def remove_second_group(m):
	            return m.group(1)
	        org_string = file
	        df['id'] = re.sub("(.*)(.{4}$)", remove_second_group, org_string)
	        #Write to CSV
	        df.to_csv(outpath+'/activity_'+file+'.csv')

get_gpx()