# Metropolis AI: Smart City Control Room

> A live control room dashboard fusing traffic, energy grid and air
> quality data for New York City — built for the Elite Tech Intern
> Internship (Dashboard Development track).

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

## Overview

Three live data feeds — traffic congestion (TomTom), electricity grid
load (EIA) and air quality (OpenAQ) — fused into a single real-time
control room view of New York City.

## Live demo

*(Link will be added once deployed)*

## Features

- [ ] Live traffic congestion feed and incident map
- [ ] Real-time electricity grid demand monitoring
- [ ] Live air quality index tracking
- [ ] Unified map-based control room view
- [ ] Auto-refreshing dashboard

## Tech stack

| Layer | Tools |
|---|---|
| Data processing | Pandas, NumPy |
| Live feeds | TomTom Traffic API, EIA API, OpenAQ API |
| Visualization | Plotly, PyDeck |
| Web app | Streamlit |

## Project structure

Metropolis_AI_Smart_City_Control_Room/
├── app/ # Streamlit application
├── data/ # Raw and processed datasets
├── notebooks/ # Exploratory work
├── src/ # Core Python modules
├── assets/ # Images and screenshots for README
├── requirements.txt
└── README.md


## Getting started

```bash
git clone https://github.com/inanbiswas10/Metropolis_AI_Smart_City_Control_Room.git
cd Metropolis_AI_Smart_City_Control_Room
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/main.py
```

## Author

Built by Inan Biswas as part of the Elite Tech Intern Internship.