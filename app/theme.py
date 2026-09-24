# app/theme.py

# Design system for the Metropolis AI Smart City Control Room.

# Palette concept: a real operations control room, not a finance
# dashboard - a dark, teal-tinted graphite background (screens are the
# main light source), with color that carries genuine operational
# meaning. Traffic and air quality share one status spectrum
# (green/amber/red) because that's the real-world convention both
# domains already use (traffic lights, EPA's Air Quality Index).
# Energy gets its own color (electric blue) since grid demand isn't a
# "good/bad" reading the way congestion or air quality is.

# Typography: Space Grotesk for headings and body, JetBrains Mono for
# every live number - an engineering/systems feel, distinct from
# Project 1's IBM Plex pairing.

import streamlit as st

COLORS = {
    "bg": "#0B1210",
    "surface": "#121C19",
    "surface_alt": "#182722",
    "border": "#223330",
    "text_primary": "#E7F1EE",
    "text_secondary": "#7FA096",
    "status_good": "#3DDC84",       # flowing traffic / good air quality
    "status_watch": "#F5A623",      # moderate congestion / moderate AQI
    "status_critical": "#E64C3C",   # heavy congestion / unhealthy AQI
    "energy": "#4FA8F5",            # electric blue - grid data, its own category
}

def get_status_color (value,good_max,watch_max):

    # Generic threshold-based status color picker, shared by the traffic
    # and air quality panels so both use the same green/amber/red logic
    # with domain-appropriate thresholds passed in by the caller.

    if value <= good_max:
        return COLORS ["status_good"]
    if value <= watch_max:
        return COLORS ["status_watch"]
    return COLORS ["status_critical"]

def get_status_label (value,good_max,watch_max,labels = ("Good","Moderate","Critical")):

    # Matching text label for get_status_color(), same thresholds.
    # Domain-specific wording is passed in - "Flowing/Moderate/Heavy" for
    # traffic reads oddly for air quality, so each panel supplies its own.

    if value <= good_max:
        return labels [0]
    if value <= watch_max:
        return labels [1]
    return labels [2]

def inject_theme ():

    # Injects fonts and CSS overrides. Call once, at the top of app/main.py. 

    st.markdown (
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {{
            --bg: {COLORS ["bg"]};
            --surface: {COLORS ["surface"]};
            --surface-alt: {COLORS ["surface_alt"]};
            --border: {COLORS ["border"]};
            --text-primary: {COLORS ["text_primary"]};
            --text-secondary: {COLORS ["text_secondary"]};
            --status-good: {COLORS ["status_good"]};
            --status-watch: {COLORS ["status_watch"]};
            --status-critical: {COLORS ["status_critical"]};
            --energy: {COLORS ["energy"]};
        }}

        .stApp {{
            background-color: var(--bg);
            font-family: 'Space Grotesk', sans-serif;
            color: var(--text-primary);
        }}

        [data-testid="stHeader"] {{
            background-color: var(--bg);
        }}

        h1, h2, h3, h4 {{
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            color: var(--text-primary);
            letter-spacing: -0.01em;
        }}

        p, span, div, label {{
            font-family: 'Space Grotesk', sans-serif;
        }}

        .control-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.9rem;
            margin-bottom: 1.5rem;
        }}
        .control-bar-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-primary);
        }}
        .control-bar-meta {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}

        .zone-panel {{
            background-color: var(--surface);
            border-top: 3px solid var(--border);
            border-radius: 4px;
            padding: 1.1rem 1.2rem;
            height: 100%;
        }}
        .zone-panel.traffic {{ border-top-color: var(--status-watch); }}
        .zone-panel.energy {{ border-top-color: var(--energy); }}
        .zone-panel.air {{ border-top-color: var(--status-good); }}

        .zone-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.8rem;
        }}

        .status-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border);
        }}
        .status-row:last-child {{ border-bottom: none; }}
        .status-row-label {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.85rem;
            color: var(--text-primary);
        }}
        .status-row-value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        .status-dot {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid var(--border);
            border-radius: 4px;
        }}
        </style>
        """,
        unsafe_allow_html = True,)