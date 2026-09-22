"""
src/traffic.py

Real traffic data module - pulls live flow data for 5 monitoring points
across New York City, each empirically validated across multiple test
runs to show genuine, repeatable congestion signal (not just proximity
to a famous landmark that happens to sit on a low-capacity local street).
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

MONITORED_POINTS = {
    "Brooklyn Bridge": (40.7061, -73.9969),
    "FDR Drive (Midtown)": (40.7484, -73.9680),
    "Lincoln Tunnel (NY approach)": (40.7614, -74.0026),
    "West Side Highway (9A) @ 42nd St": (40.7648, -74.0018),
    "Cross Bronx Expressway": (40.8448, -73.9048),
}


def get_traffic_snapshot():
    """
    Fetches live flow data for every monitored point and returns a list
    of dicts, one per location, with a computed congestion percentage:
    0% = moving at free-flow speed, higher % = more congested.
    """
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    results = []

    for name, (lat, lon) in MONITORED_POINTS.items():
        params = {"key": TOMTOM_API_KEY, "point": f"{lat},{lon}"}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            segment = response.json()["flowSegmentData"]

            current_speed = segment["currentSpeed"]
            free_flow_speed = segment["freeFlowSpeed"]

            if free_flow_speed > 0:
                congestion_pct = round((1 - current_speed / free_flow_speed) * 100, 1)
            else:
                congestion_pct = 100.0

            results.append({
                "location": name,
                "latitude": lat,
                "longitude": lon,
                "current_speed_kmh": current_speed,
                "free_flow_speed_kmh": free_flow_speed,
                "congestion_pct": congestion_pct,
                "road_closed": segment["roadClosure"],
                "confidence": segment["confidence"],
            })

        except requests.RequestException as e:
            results.append({
                "location": name,
                "latitude": lat,
                "longitude": lon,
                "error": str(e),
            })

    return results


if __name__ == "__main__":
    snapshot = get_traffic_snapshot()
    for point in snapshot:
        if "error" in point:
            print(f"{point['location']}: FAILED - {point['error']}")
        else:
            print(
                f"{point['location']}: {point['current_speed_kmh']} km/h "
                f"(free-flow {point['free_flow_speed_kmh']} km/h) - "
                f"{point['congestion_pct']}% congested"
            )