"""
src/air_quality.py

Real air quality data module - finds actively-reporting monitoring
stations near New York City and pulls their latest sensor readings.

Filters out stale stations (flagged during Day 1 testing - some OpenAQ
stations near NYC haven't reported since 2017) rather than trusting
proximity alone.
"""

import os
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

LATITUDE = 40.7128
LONGITUDE = -74.0060
SEARCH_RADIUS_METERS = 25000
MAX_STATIONS = 5

RECENCY_WINDOW = timedelta(hours=48)


def _find_active_stations():
    """
    Searches for monitoring stations near NYC, then filters to only
    those with a recent datetimeLast - excludes stations that are
    geographically close but haven't actually reported in years.
    """
    url = "https://api.openaq.org/v3/locations"
    headers = {"X-API-Key": OPENAQ_API_KEY}
    params = {
        "coordinates": f"{LATITUDE},{LONGITUDE}",
        "radius": SEARCH_RADIUS_METERS,
        "limit": 20,
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    all_stations = response.json()["results"]

    cutoff = datetime.now(timezone.utc) - RECENCY_WINDOW
    active = []

    for station in all_stations:
        last_seen_str = station.get("datetimeLast", {}).get("utc")
        if not last_seen_str:
            continue

        # Python 3.11+ parses a trailing "Z" directly - no manual string
        # replacement needed, which also removes the exact fragile
        # string literal that got corrupted above
        last_seen = datetime.fromisoformat(last_seen_str)
        if last_seen >= cutoff:
            active.append(station)

    return active[:MAX_STATIONS]


def get_air_quality_snapshot():
    """
    Returns a list of dicts, one per actively-reporting station near
    NYC, each with its latest readings for whatever pollutants that
    station measures.
    """
    headers = {"X-API-Key": OPENAQ_API_KEY}
    stations = _find_active_stations()
    results = []

    for station in stations:
        station_id = station["id"]
        latest_url = f"https://api.openaq.org/v3/locations/{station_id}/latest"

        try:
            response = requests.get(latest_url, headers=headers, timeout=10)
            response.raise_for_status()
            readings_raw = response.json()["results"]

            sensor_lookup = {s["id"]: s["parameter"] for s in station["sensors"]}

            readings = []
            for r in readings_raw:
                param = sensor_lookup.get(r["sensorsId"], {})
                readings.append({
                    "parameter": param.get("displayName", "unknown"),
                    "value": r["value"],
                    "units": param.get("units", ""),
                    "measured_at_utc": r["datetime"]["utc"],
                })

            results.append({
                "station": station["name"],
                "distance_km": round(station["distance"] / 1000, 1),
                "readings": readings,
            })

        except requests.RequestException as e:
            results.append({"station": station["name"], "error": str(e)})

        except KeyError as e:
            print(f"\nUnexpected response shape for {station['name']} - raw response:")
            print(response.text)
            results.append({"station": station["name"], "error": f"KeyError: {e}"})

    return results


if __name__ == "__main__":
    snapshot = get_air_quality_snapshot()

    if not snapshot:
        print("No actively-reporting stations found within the search radius.")
    else:
        for station in snapshot:
            if "error" in station:
                print(f"{station['station']}: FAILED - {station['error']}")
                continue

            print(f"{station['station']} ({station['distance_km']} km away):")
            if not station["readings"]:
                print("  No current readings available")
            for reading in station["readings"]:
                print(f"  {reading['parameter']}: {reading['value']} {reading['units']}")