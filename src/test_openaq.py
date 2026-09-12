# src/test_openaq.py

# Quick connectivity test for the OpenAQ API v3. Finds air quality
# monitoring stations near New York City to confirm the API key works.

import os
import requests
from dotenv import load_dotenv

load_dotenv ()

OPENAQ_API_KEY = os.getenv ("OPENAQ_API_KEY")

# Manhattan, NYC

LATITUDE = 40.7128
LONGITUDE = -74.0060

def main_function ():

    url = "https://api.openaq.org/v3/locations"
    headers = {"X-API-Key": OPENAQ_API_KEY}
    params = {
        "coordinates": f"{LATITUDE},{LONGITUDE}",
        "radius": 25000,  # meters - 25km search radius around NYC
        "limit": 5,
    }

    response = requests.get (url,headers = headers,params = params,timeout = 10)

    # Same lesson from the EIA debugging - print the raw response before
    # raising on a bad status, so we can see exactly what OpenAQ says if
    # something's wrong, instead of just getting a bare exception.

    print (f"HTTP status code: {response.status_code}")
    print ("Raw response body:")
    print (response.text)

    response.raise_for_status ()
    data = response.json ()

    results = data.get ("results",[])
    print (f"\nParsed - found {len (results)} monitoring station(s) near NYC:")
    for station in results:
        print (f"  {station ['name']} (id = {station ['id']})")

if __name__ == "__main__":
    main_function ()