# app/main.py

# Metropolis AI: Smart City Control Room - main Streamlit application.

import os
import sys

sys.path.insert (0,os.path.dirname (os.path.abspath (__file__)))

import streamlit as st

# Bridge Streamlit Cloud secrets into os.environ BEFORE importing our
# data modules - they read API keys via os.getenv() at import time.
# Streamlit's docs say root-level secrets become env vars automatically,
# but that's been unreliable across versions in the past, so we do it
# explicitly here instead of depending on it. Wrapped in try/except
# because locally there's no secrets.toml at all - .env covers that case.

try:
    for _key in ("TOMTOM_API_KEY","EIA_API_KEY","OPENAQ_API_KEY"):
        if _key in st.secrets and _key not in os.environ:
            os.environ [_key] = st.secrets [_key]
except Exception:
    pass

from theme import inject_theme,COLORS
from data_loader import load_traffic,load_energy,load_air_quality
from map_view import build_map
from panels import render_traffic_panel,render_energy_panel,render_air_quality_panel

st.set_page_config (
    page_title = "Metropolis AI: Smart City Control Room",
    page_icon = "🗺️",
    layout = "wide",
    initial_sidebar_state = "collapsed",
)
inject_theme ()

_, refresh_col = st.columns ([6,1])
with refresh_col:
    if st.button ("\u21bb Refresh",use_container_width = True):
        st.cache_data.clear ()
        st.rerun ()

traffic = load_traffic ()
energy = load_energy ()
air_quality = load_air_quality ()

TRAFFIC_WATCH_MAX = 50
AQI_MODERATE_MAX = 35.4

alert_count = 0
for point in traffic:
    if "error" not in point and point ["congestion_pct"] > TRAFFIC_WATCH_MAX:
        alert_count += 1
for station in air_quality:
    if "error" not in station:
        pm25 = next ((r for r in station ["readings"] if r ["parameter"] == "PM2.5"),None)
        if pm25 and pm25 ["value"] > AQI_MODERATE_MAX:
            alert_count += 1

status_text = "ALL NOMINAL" if alert_count == 0 else f"{alert_count} ACTIVE ALERT{'S' if alert_count != 1 else ''}"
status_color = COLORS ["status_good"] if alert_count == 0 else COLORS ["status_critical"]

from datetime import datetime
now_str = datetime.now ().strftime ("%b %d, %Y \u00b7 %I:%M %p")

st.markdown (
    f"""
    <div class="control-bar">
        <div class="control-bar-title">Metropolis AI \u00b7 Smart City Control Room</div>
        <div class="control-bar-meta">
            <span style="color:{status_color};">\u25cf {status_text}</span>
            &nbsp;&nbsp;|&nbsp;&nbsp;{now_str}
        </div>
    </div>
    """,
    unsafe_allow_html = True,)

deck = build_map (traffic,air_quality)
st.pydeck_chart (deck)

st.markdown ("<div style='height: 1.5rem;'></div>",unsafe_allow_html = True)
col1,col2,col3 = st.columns (3)

with col1:
    st.markdown (render_traffic_panel (traffic),unsafe_allow_html = True)
with col2:
    st.markdown (render_energy_panel (energy),unsafe_allow_html = True)
with col3:
    st.markdown (render_air_quality_panel (air_quality),unsafe_allow_html = True)