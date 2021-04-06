import pandas as pd
import requests
import json
import time
import csv
import glob
import datetime as dt


# Get the tokens from file
with open('strava_tokens.json') as json:
    my_tokens = json.load(json)


# If access_token has expired then use the refresh_token to get the new access_token
if my_tokens['expires_at'] < time.time():
# Call Strava API with current refresh token
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': '*',
                                'client_secret': '*',
                                'grant_type': 'refresh_token',
                                'refresh_token': my_tokens['refresh_token']
                                }
                    )
# Token response variable
    new_tokens = response.json()
# Save new tokens in json
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_tokens, outfile)
# Rewrite tokens after refresh
    my_tokens = new_tokens




# Get activities (all pages)
page = 1
url = "https://www.strava.com/api/v3/activities"
access_token = strava_tokens['access_token']
# Create the df [ I removed fields that I do not need ]
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
	"max_speed"
    ]
)

while True:
    
    # get page n of activities from Strava
    r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
    r = r.json()
    
    # if results do not exist then exit loop
    if (not r):
        break
    
    # else add data to dataframe
    for column in activities:
    	for x in range(len(r)):
        	activities.loc[x + (page-1)*200,column] = r[x][column]
       
    # extend to all pages of activity 
    page += 1

# Export activities as a csv 
activities.to_csv('/Users/jackhulbert/Desktop/Data Science Projects/Strava/Data/strava_activities.csv')

