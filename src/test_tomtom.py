# src/test_tomtom.py

# Quick connectivity test for the TomTom Traffic API. Pulls live flow
# data for a single road segment near Times Square, NYC to confirm the
# API key works before building anything else on top of it.

import os
import requests
from dotenv import load_dotenv

load_dotenv ()

TOMTOM_API_KEY = os.getenv ("TOMTOM_API_KEY")

# Times Square, NYC - a coordinate with reliably high traffic volume

LATITUDE = 40.7580
LONGITUDE = -73.9855

def main_function ():

    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    params = {
        "key": TOMTOM_API_KEY,
        "point": f"{LATITUDE},{LONGITUDE}",
    }

    response = requests.get (url,params = params,timeout = 10)
    response.raise_for_status ()
    data = response.json ()

    print ("TomTom connection: SUCCESS (got a 200 response) !!")
    print ("\nRaw response:")
    print (data)

    # Also try to pull out the specific fields we'll use in the dashboard.
    # Printing the raw response above too, in case the actual field names
    # differ slightly from what the docs describe.

    try:
        segment = data ["flowSegmentData"]
        print ("\nParsed:")
        print (f"  Current speed:       {segment ['currentSpeed']} km/h")
        print (f"  Free-flow speed:     {segment ['freeFlowSpeed']} km/h")
        print (f"  Current travel time: {segment ['currentTravelTime']} seconds")
    except KeyError as e:
        print (f"\nCouldn't find expected field {e} - check the raw response above")

if __name__ == "__main__":
    main_function ()