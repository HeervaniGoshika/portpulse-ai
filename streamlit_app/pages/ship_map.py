import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import pydeck as pdk
import time
from src.data_loader import load_ais_data

st.title("🚢 Live Ship Map")

# Load data FIRST
df = load_ais_data("data/processed/sample.csv")

# Sort timestamps
timestamps = sorted(df["timestamp"].unique())

# Placeholder for animation
placeholder = st.empty()

for t in timestamps[:50]:
    current = df[df["timestamp"] == t]

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=current,
        get_position='[lon, lat]',
        get_radius=250,
        get_fill_color='[200, 30, 0]',
        pickable=True,
    )

    view = pdk.ViewState(
        latitude=17.5, 
        longitude=84.5, 
        zoom=6, 
        pitch=40
    )

    tooltip = {"text": "MMSI: {MMSI}\nSpeed: {SOG}"}

    placeholder.pydeck_chart(
        pdk.Deck(layers=[layer], initial_view_state=view, tooltip=tooltip)
    )

    time.sleep(0.5)