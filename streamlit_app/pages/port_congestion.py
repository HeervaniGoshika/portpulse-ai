import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from src.data_loader import load_ais_data
from src.preprocessing import clean_ais
from src.feature_engineering import add_velocity, add_distance_to_port
from src.congestion_model import detect_congestion

PORT_LAT = 17.6868
PORT_LON = 83.2185

df = load_ais_data("data/processed/sample.csv")
df = clean_ais(df)
df = add_velocity(df)
df = add_distance_to_port(df, PORT_LAT, PORT_LON)

level, near, waiting = detect_congestion(df)

st.header("Port Congestion")
st.metric("Congestion Level", level)
st.write("Ships near port:", len(near))
st.write("Waiting ships:", len(waiting))