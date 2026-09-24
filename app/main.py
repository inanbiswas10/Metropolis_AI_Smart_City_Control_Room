# app/main.py

# Metropolis AI: Smart City Control Room - main Streamlit application.

import os
import sys
from datetime import datetime

sys.path.insert (0,os.path.dirname (os.path.abspath (__file__)))

import streamlit as st

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

traffic = load_traffic ()
energy = load_energy ()
air_quality = load_air_quality ()

# Aggregate alert count for the control bar - same thresholds panels.py
# and map_view.py already use for coloring individual readings, so the
# top-level status always agrees with what the panels show underneath

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