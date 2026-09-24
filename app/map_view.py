# app/map_view.py

# Builds the hero live map: NYC traffic points and air quality stations,
# each colored by real-time status using the shared green/amber/red
# convention from theme.py. Returns a pydeck.Deck object - main.py is
# responsible for actually rendering it via st.pydeck_chart ().

import math

import pydeck as pdk

from theme import get_status_color

TRAFFIC_GOOD_MAX = 25
TRAFFIC_WATCH_MAX = 50

# Real EPA PM2.5 breakpoints (µg/m³) for "Good" and "Moderate" AQI
# categories. Note: EPA's official AQI uses a 24-hour average - what we
# have here is a single latest instantaneous reading, so this
# approximates the AQI color convention rather than computing an
# official AQI value. Worth being upfront about that distinction.

AQI_GOOD_MAX = 12.0
AQI_MODERATE_MAX = 35.4


def _hex_to_rgb(hex_color):

    # Converts a '#RRGGBB' string to an [r, g, b] list for pydeck.

    hex_color = hex_color.lstrip ("#")
    return [int (hex_color [i:i + 2],16) for i in (0,2,4)]

def _build_traffic_points (traffic_snapshot):

    points = []
    for point in traffic_snapshot:
        if "error" in point:
            continue
        color = get_status_color (point ["congestion_pct"],TRAFFIC_GOOD_MAX,TRAFFIC_WATCH_MAX)
        points.append ({
            "lon": point ["longitude"],
            "lat": point ["latitude"],
            "label": point ["location"],
            "detail": f"{point ['congestion_pct']} % congested",
            "color": _hex_to_rgb (color),
        })
    return points

def _build_air_quality_points (air_quality_snapshot):
    points = []
    for station in air_quality_snapshot:
        if "error" in station or "latitude" not in station:
            continue
        pm25 = next ((r for r in station ["readings"] if r ["parameter"] == "PM2.5"),None)
        if pm25 is None:
            continue

        color = get_status_color (pm25 ["value"],AQI_GOOD_MAX,AQI_MODERATE_MAX)
        points.append ({
            "lon": station ["longitude"],
            "lat": station ["latitude"],
            "label": station ["station"],
            "detail": f"PM2.5: {pm25 ['value']} \u00b5g/m\u00b3",
            "color": _hex_to_rgb (color),
        })
    return points

def _compute_view_state (points,padding_factor = 1.4):

    # Computes a view that tightly fits every point, with some padding so
    # markers aren't flush against the map edge. Calculated manually
    # (standard bounding-box-to-zoom approximation) rather than relying
    # on an undocumented library helper we haven't verified ourselves.
    
    lats = [p ["lat"] for p in points]
    lons = [p ["lon"] for p in points]

    center_lat = (max (lats) + min (lats)) / 2
    center_lon = (max (lons) + min (lons)) / 2

    lat_span = (max (lats) - min (lats)) * padding_factor
    lon_span = (max (lons) - min (lons)) * padding_factor
    span = max (lat_span,lon_span,0.01)  # avoid log (0) if points coincide

    zoom = math.log2 (360 / span)-1
    zoom = max (9,min (zoom,14))  # clamp to a sane range either way

    return pdk.ViewState (latitude = center_lat,longitude = center_lon,zoom = zoom,pitch = 0)

def build_map (traffic_snapshot,air_quality_snapshot):

    # Returns a pydeck.Deck with two layers - traffic points and air
    # quality stations - ready to pass straight to st.pydeck_chart().
    # The view auto-fits to the actual data instead of a hardcoded
    # center/zoom, so it stays correct even if we add or move points later.
    
    traffic_points = _build_traffic_points (traffic_snapshot)
    air_points = _build_air_quality_points (air_quality_snapshot)
    all_points = traffic_points + air_points

    traffic_layer = pdk.Layer (
        "ScatterplotLayer",
        data = traffic_points,
        get_position = ["lon","lat"],
        get_fill_color = "color",
        get_radius = 200,
        pickable = True,
        opacity = 0.85,
    )

    air_layer = pdk.Layer (
        "ScatterplotLayer",
        data = air_points,
        get_position = ["lon","lat"],
        get_fill_color = "color",
        get_radius = 120,
        pickable = True,
        opacity = 0.85,
        stroked = True,
        get_line_color = [231,241,238],
        line_width_min_pixels = 1,
    )

    if all_points:
        view_state = _compute_view_state (all_points)
    else:
        # Fallback only if every point failed to load - shouldn't happen
        # given our upstream error handling, but a sane default beats a
        # broken/empty map
        view_state = pdk.ViewState (latitude = 40.75,longitude = -73.97,zoom = 10.5,pitch = 0)

    return pdk.Deck (
        layers = [traffic_layer,air_layer],
        initial_view_state = view_state,
        map_style = pdk.map_styles.DARK,
        tooltip = {"text": "{label}\n{detail}"},)