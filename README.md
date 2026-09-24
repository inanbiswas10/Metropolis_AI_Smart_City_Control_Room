# Metropolis AI: Smart City Control Room

> A live operations dashboard fusing real time traffic, electricity
> grid and air quality data into a single control room view of New
> York City — built for the Elite Tech Intern Internship (Dashboard
> Development track).

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Complete-2DB88A)

## Overview

Three genuinely live data feeds — traffic congestion (TomTom), NYISO
electricity grid demand (EIA) and air quality (OpenAQ) — fused into
one real-time control room with a live map as the centerpiece rather
than a static report.

## Live demo

**[Open the live control room](https://metropolis-ai-smart-city-control-room.streamlit.app/)**

## Engineering notes

A few real issues surfaced and fixed during development, rather than
smoothed over:

- **Not every nearby air quality station is still active.** One
  station near NYC hadn't reported since 2017 despite being
  geographically closest — the air quality module explicitly filters
  for stations that reported within the last 48 hours before trusting
  them.
- **Landmark proximity isn't the same as a meaningful traffic signal.**
  An early version anchored a monitoring point to Times Square's
  pedestrian plaza, which has a free-flow speed of ~ 10-17 km/h
  regardless of actual traffic — real congestion couldn't register at
  that resolution. The 5 final traffic points were empirically
  validated across multiple live test runs to confirm each shows
  genuine, repeatable congestion signal.
- **Map zoom uses pydeck's own `compute_view()` utility**, not a
  hand rolled formula — an earlier hand written zoom calculation was
  measurably too imprecise for a tightly clustered set of points.

## Features

- [x] Live traffic congestion across 5 validated NYC points (TomTom)
- [x] Real-time NYISO electricity grid demand with 24h trend (EIA)
- [x] Live air quality (PM2.5) from actively-reporting stations (OpenAQ)
- [x] Unified map with color-coded status markers
- [x] Manual refresh control to pull fresh data on demand
- [x] Aggregate alert counter in the control bar

## Tech stack

| Layer | Tools |
|---|---|
| Live data | TomTom Traffic API, EIA API (NYISO), OpenAQ API |
| Mapping | PyDeck |
| Web app | Streamlit |

## Project structure

Metropolis_AI_Smart_City_Control_Room/
├── app/
│ ├── main.py # Streamlit entry point
│ ├── theme.py # Design system: colors, fonts, CSS
│ ├── data_loader.py # Cached wiring to the real data modules
│ ├── map_view.py # Live map builder (pydeck)
│ └── panels.py # Zone panel HTML builders
├── src/
│ ├── traffic.py # TomTom live traffic module
│ ├── energy.py # EIA live grid module
│ └── air_quality.py # OpenAQ live air quality module
├── requirements.txt
└── README.md


## Getting started

```bash
git clone https://github.com/inanbiswas10/Metropolis_AI_Smart_City_Control_Room.git
cd Metropolis_AI_Smart_City_Control_Room
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your own free API keys from
TomTom, EIA and OpenAQ then run:

```bash
streamlit run app/main.py
```

## Data sources

- [TomTom Traffic API](https://developer.tomtom.com) — live flow data
- [EIA API](https://www.eia.gov/opendata/) — NYISO hourly grid demand
- [OpenAQ API](https://explore.openaq.org) — live air quality monitoring

## Author

Built by Inan Biswas as part of the Elite Tech Intern Internship.