"""
app/data_loader.py

Wires the three real data modules (src/traffic.py, src/energy.py,
src/air_quality.py) into the Streamlit app, with caching so the
dashboard stays fast and doesn't hammer any API's rate limit on every
rerun.

Cache durations are set per source based on how often the underlying
data actually changes:
- Traffic: fastest (2 min) - conditions genuinely change minute to minute
- Air quality: moderate (10 min) - government reference monitors report hourly-ish
- Energy grid: slowest (15 min) - EIA itself only publishes a new hourly reading once an hour
"""

import os
import sys

# Add ../src to the import path so we can import our real data modules
# as flat imports. Same lesson as Project 1: don't assume a directory
# is automatically importable just because it worked once locally -
# make it explicit so it works the same way everywhere.
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, os.path.abspath(SRC_DIR))

import streamlit as st

from traffic import get_traffic_snapshot
from energy import get_grid_snapshot
from air_quality import get_air_quality_snapshot


@st.cache_data(ttl=120)
def load_traffic():
    """Live traffic snapshot, refreshed at most every 2 minutes."""
    return get_traffic_snapshot()


@st.cache_data(ttl=900)
def load_energy():
    """NYISO grid snapshot, refreshed at most every 15 minutes."""
    return get_grid_snapshot()


@st.cache_data(ttl=600)
def load_air_quality():
    """Live air quality snapshot, refreshed at most every 10 minutes."""
    return get_air_quality_snapshot()


if __name__ == "__main__":
    # Quick smoke test - confirms the cross-folder imports and all
    # three underlying modules work together before we build any UI
    # on top of them.
    print("Testing traffic loader...")
    traffic = load_traffic()
    print(f"  Got {len(traffic)} traffic points")

    print("\nTesting energy loader...")
    energy = load_energy()
    print(f"  Current NYISO demand: {energy.get('current_demand_mwh', 'N/A')} MWh")

    print("\nTesting air quality loader...")
    air = load_air_quality()
    print(f"  Got {len(air)} air quality stations")