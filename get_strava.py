
#############################################################################################
# Get Strava                                                                  
# by Jack Hulbert                                                                         
# April 2020                                                                                
# https://github.com/jackhulbertpdx/strava                        
# ----------------------------------------------------------------------------------------- 
# This script allows one to dynamically load refresh tokens with their Strava credentials 
# , loop through all pages of activity data from a Strava profile, and write all activities
# to a csv output.
# Special thanks to Benji Knights Johnson for writing an easy to follow article on Medium 
# (https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86)
#############################################################################################






import pandas as pd
import requests
import json
import time
import csv
import glob
import datetime as dt
import io
from io import StringIO


# Get the tokens from json file to connect with Strava
with open('strava_tokens.json') as json_file:
    tokens = json.load(json_file)


# If has expired then use the refresh_token to get the new token

if tokens['expires_at'] < time.time():

# Make Strava auth API call with current token
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': 'my_id',
                                'client_secret': 'my_secret',
                                'grant_type': 'refresh_token',
                                'refresh_token': tokens['refresh_token']
                                }
                    )

# Save response as new variable
    new_tokens = response.json()
# Save new tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_tokens, outfile)
# Use new tokens
    tokens = new_tokens




# Loop through all activities in Strava feed

url = "https://www.strava.com/api/v3/activities"
access_token = tokens['access_token']
page = 1
# Create the dataframe with your desired fields
activities = pd.DataFrame(
    columns = ["name",
    "distance",
	"moving_time",
	"elapsed_time",
	"total_elevation_gain",
	"type",
	"id",
	"external_id",
	"upload_id",
	"start_date",
	"start_latlng",
	"end_latlng",
	"location_city",
	"location_state",
	"location_country",
	"start_latitude",
	"start_longitude",
	"average_speed",
	"max_speed",

    ]
)

while True:
    
    # Get all pages of activities from Strava

    r = requests.get(url + '?access_token=' + access_token + '&per_page=100' + '&page=' + str(page))
    r = r.json()
    
    #if no results then exit loop
    if (not r):
        break
    
    # otherwise append new data to dataframe
    for column in activities:
    	for x in range(len(r)):
        	activities.loc[x + (page-1)*200,column] = r[x][column]
       
    # increment page
    page += 1

# Export activities as a csv 

activities.to_csv('strava_activities.csv')

#
