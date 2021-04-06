import pandas as pd
import requests
import json
import time
import csv
import glob
import datetime as dt
import io
from io import StringIO
import psycopg2


# Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)


## If access_token has expired then use the refresh_token to get the new access_token
if strava_tokens['expires_at'] < time.time():
#Make Strava auth API call with current refresh token
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': '63186',
                                'client_secret': 'ad5fc192891cacdd774b70da8cc389c532837067',
                                'grant_type': 'refresh_token',
                                'refresh_token': strava_tokens['refresh_token']
                                }
                    )
#Save response as json in new variable
    new_strava_tokens = response.json()
# Save new tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_strava_tokens, outfile)
#Use new Strava tokens from now
    strava_tokens = new_strava_tokens




# Loop through all activities
page = 1
url = "https://www.strava.com/api/v3/activities"
access_token = strava_tokens['access_token']
# Create the dataframe ready for the API call to store your activity data
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
    
    # get page of activities from Strava
    r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
    r = r.json()
    
    # if no results then exit loop
    if (not r):
        break
    
    # otherwise add new data to dataframe
    for column in activities:
    	for x in range(len(r)):
        	activities.loc[x + (page-1)*200,column] = r[x][column]
       
    # increment page
    page += 1
# Export your activities file as a csv 
# to the folder you're running this script in



activities.to_csv('/Users/jackhulbert/Desktop/Data Science Projects/Strava/Data/strava_activities.csv')

#