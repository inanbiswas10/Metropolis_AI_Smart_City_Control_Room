# src/test_eia.py

# Quick connectivity test for the EIA API v2. Pulls the 5 most recent
# hourly electricity demand readings for NYISO (New York's balancing
# authority) to confirm the API key works.

import os
import requests
from dotenv import load_dotenv

load_dotenv()

EIA_API_KEY = os.getenv ("EIA_API_KEY")

def main_function ():

    url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
    params = {
        "api_key": EIA_API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "facets[respondent][]": "NYIS",  # New York Independent System Operator
        "facets[type][]": "D",           # D = Demand
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": "0",
        "length": "5",
    }

    response = requests.get (url,params = params,timeout = 10)

    # Print the raw response BEFORE raising on a bad status code - EIA
    # usually sends a JSON body explaining exactly what went wrong, and
    # raise_for_status() throws before we'd ever get to see it.

    print (f"HTTP status code: {response.status_code}")
    print ("Raw response body:")
    print (response.text)

    response.raise_for_status ()

    data = response.json ()
    readings = data ["response"]["data"]
    print (f"\nParsed - {len (readings)} recent hourly demand readings for NYISO:")
    for row in readings:
        print (f"  {row['period']}: {row['value']} MWh")

if __name__ == "__main__":
    main_function ()