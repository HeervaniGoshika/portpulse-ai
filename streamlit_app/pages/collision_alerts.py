import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from src.collision_engine import detect_collisions
from src.data_loader import load_ais_data
from src.feature_engineering import add_velocity

df = load_ais_data("data/processed/sample.csv")

df = add_velocity(df)

alerts = detect_collisions(df)

st.header("Collision Alerts")

if alerts:
    for a in alerts:
        st.error(f"⚠️ Risk between {a[0]} and {a[1]} | CPA={a[2]:.2f}")
else:
    st.success("No collision risks")
