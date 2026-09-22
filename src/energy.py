"""
src/energy.py

Real energy grid data module - pulls the most recent 24 hourly
electricity demand readings for NYISO (New York's balancing authority)
and returns a clean, structured summary the dashboard can use directly.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

EIA_API_KEY = os.getenv("EIA_API_KEY")

RESPONDENT = "NYIS"  # New York Independent System Operator
HOURS_TO_FETCH = 24


def get_grid_snapshot():
    """
    Fetches the most recent 24 hourly demand readings for NYISO and
    returns a dict with the current reading, a 24-hour average, how far
    current demand sits above/below that average, and a short-term
    trend based on the last two readings.
    """
    url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
    params = {
        "api_key": EIA_API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "facets[respondent][]": RESPONDENT,
        "facets[type][]": "D",  # D = Demand
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": "0",
        "length": str(HOURS_TO_FETCH),
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        rows = response.json()["response"]["data"]

        # Filter out any row with a missing/null value defensively -
        # rather than assume every row EIA returns is guaranteed usable,
        # this guards the math below either way
        readings = [
            {"period": row["period"], "value_mwh": float(row["value"])}
            for row in rows
            if row["value"] not in (None, "")
        ]

        if not readings:
            return {"error": "No valid readings returned"}

        current = readings[0]["value_mwh"]
        avg_24h = round(sum(r["value_mwh"] for r in readings) / len(readings), 1)
        pct_vs_avg = round(((current - avg_24h) / avg_24h) * 100, 1)

        # Readings are newest-first, so index 0 vs 1 gives short-term trend
        if len(readings) >= 2:
            previous = readings[1]["value_mwh"]
            if current > previous:
                trend = "rising"
            elif current < previous:
                trend = "falling"
            else:
                trend = "stable"
        else:
            trend = "unknown"

        return {
            "respondent": RESPONDENT,
            "current_demand_mwh": current,
            "current_period": readings[0]["period"],
            "avg_24h_mwh": avg_24h,
            "pct_vs_24h_avg": pct_vs_avg,
            "trend": trend,
            "readings": readings,
        }

    except requests.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    snapshot = get_grid_snapshot()

    if "error" in snapshot:
        print(f"FAILED: {snapshot['error']}")
    else:
        print(f"NYISO grid snapshot (as of {snapshot['current_period']}):")
        print(f"  Current demand:   {snapshot['current_demand_mwh']:,.0f} MWh")
        print(f"  24-hour average:  {snapshot['avg_24h_mwh']:,.0f} MWh")
        print(f"  Vs. 24h average:  {snapshot['pct_vs_24h_avg']:+.1f}%")
        print(f"  Trend:            {snapshot['trend']}")