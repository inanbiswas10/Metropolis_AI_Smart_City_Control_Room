# app/panels.py

# Builds the HTML for the three zone panels (Traffic, Energy, Air
# Quality), reusing the shared theme classes so each panel reads as part
# of the same control room, identified by a single accent stripe rather
# than a boxed "SaaS card."

from theme import COLORS,get_status_color,get_status_label

TRAFFIC_GOOD_MAX = 25
TRAFFIC_WATCH_MAX = 50
AQI_GOOD_MAX = 12.0
AQI_MODERATE_MAX = 35.4

def _unavailable_row (label):
    return (
        f'<div class="status-row">'
        f'<span class="status-row-label">{label}</span>'
        f'<span class="status-row-value" style="color:{COLORS ["text_secondary"]};">unavailable</span>'
        f'</div>'
    )

def render_traffic_panel (traffic_snapshot):
    rows_html = ""
    for point in traffic_snapshot:
        if "error" in point:
            rows_html += _unavailable_row (point ["location"])
            continue

        color = get_status_color (point ["congestion_pct"],TRAFFIC_GOOD_MAX,TRAFFIC_WATCH_MAX)
        label = get_status_label (
            point ["congestion_pct"],TRAFFIC_GOOD_MAX,TRAFFIC_WATCH_MAX,
            labels = ("Flowing","Moderate","Heavy"),
        )
        rows_html += (
            f'<div class="status-row">'
            f'<span class="status-row-label"><span class="status-dot" style="background-color:{color};"></span>{point["location"]}</span>'
            f'<span class="status-row-value" style="color:{color};">{point ["congestion_pct"]} % \u00b7 {label}</span>'
            f'</div>'
        )
    return f'<div class="zone-panel traffic"><div class="zone-title">Traffic</div>{rows_html}</div>'

def render_energy_panel (energy_snapshot):
    if "error" in energy_snapshot:
        return f'<div class="zone-panel energy"><div class="zone-title">Energy Grid</div>{_unavailable_row ("NYISO grid")}</div>'

    trend_arrow = {"rising": "\u2191","falling": "\u2193","stable": "\u2192"}.get (energy_snapshot ["trend"],"")
    rows = [
        ("Current demand",f'{energy_snapshot ["current_demand_mwh"]:,.0f} MWh'),
        ("24h average",f'{energy_snapshot ["avg_24h_mwh"]:,.0f} MWh'),
        ("vs 24h average",f'{energy_snapshot ["pct_vs_24h_avg"]:+.1f} %'),
        ("Trend",f'{energy_snapshot ["trend"].capitalize ()} {trend_arrow}'),
    ]
    rows_html = "".join (
        f'<div class="status-row">'
        f'<span class="status-row-label"><span class="status-dot" style="background-color:{COLORS ["energy"]};"></span>{label}</span>'
        f'<span class="status-row-value" style="color:{COLORS ["energy"]};">{value}</span>'
        f'</div>'
        for label, value in rows
    )
    return f'<div class="zone-panel energy"><div class="zone-title">Energy Grid \u00b7 NYISO</div>{rows_html}</div>'

def render_air_quality_panel (air_quality_snapshot):
    rows_html = ""
    for station in air_quality_snapshot:
        if "error" in station:
            rows_html += _unavailable_row (station ["station"])
            continue

        pm25 = next ((r for r in station ["readings"] if r ["parameter"] == "PM2.5"),None)
        if pm25 is None:
            rows_html += _unavailable_row (f'{station ["station"]} (no PM2.5 sensor)')
            continue

        color = get_status_color (pm25 ["value"],AQI_GOOD_MAX,AQI_MODERATE_MAX)
        label = get_status_label (
            pm25 ["value"],AQI_GOOD_MAX,AQI_MODERATE_MAX,
            labels = ("Good","Moderate","Unhealthy"),
        )
        rows_html += (
            f'<div class="status-row">'
            f'<span class="status-row-label"><span class="status-dot" style="background-color:{color};"></span>{station ["station"]}</span>'
            f'<span class="status-row-value" style="color:{color};">{pm25 ["value"]} \u00b5g/m\u00b3 \u00b7 {label}</span>'
            f'</div>'
        )
    return f'<div class="zone-panel air"><div class="zone-title">Air Quality \u00b7 PM2.5</div>{rows_html}</div>'