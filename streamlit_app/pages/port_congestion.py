import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px


from src.data_loader import load_ais_data 
from src.preprocessing import clean_ais
from src.feature_engineering import add_velocity, add_distance_to_port
from src.feature_engineering import add_port_geofence, add_waiting_time
from src.congestion_model import (
    add_near_port_column,
    compute_congestion_features,
    rule_congestion_level,
    build_ml_features,
    congestion_over_time,
    predict_next_congestion
)

# CONFIG

PORT_LAT = 17.6868
PORT_LON = 83.2185
MODEL_PATH = "models/congestion_model.pkl"

st.set_page_config(layout="wide")
st.title("⚓ Port Congestion Analyzer")

# LOAD DATA

df = load_ais_data("data/processed/raw.csv")
df = df[df["lon"] > 83.2]

df = clean_ais(df)
df = add_velocity(df)
df = add_distance_to_port(df, PORT_LAT, PORT_LON)
df = add_port_geofence(df, PORT_LAT, PORT_LON)
df = add_waiting_time(df)

port_lat = 17.6835
port_lon = 83.2185

df = add_near_port_column(df, port_lat, port_lon)

ships_near, waiting_ships, avg_wait = compute_congestion_features(df)

# RULE-BASED CONGESTION

ships_near, waiting_ships, avg_wait = compute_congestion_features(df)

level = rule_congestion_level(ships_near, waiting_ships, avg_wait)

# st.write(df.columns)

# DISPLAY METRICS

c1, c2, c3 = st.columns(3)

c1.metric("Ships Near Port", ships_near)
c2.metric("Waiting Ships (>1hr)", waiting_ships)
c3.metric("Avg Wait (min)", round(avg_wait, 2))

st.subheader("Current Congestion Status")

if level == "HIGH":
    st.error("⚠️ HIGH CONGESTION")
elif level == "MEDIUM":
    st.warning("⚓ MEDIUM CONGESTION")
else:
    st.success("✅ LOW CONGESTION")

trend_df = congestion_over_time(df)

fig = px.line(trend_df,
              x="timestamp",
              y="waiting_ships",
              title="Waiting Ships Over Time")

st.plotly_chart(fig, width="stretch")

future_level = predict_next_congestion(trend_df)

st.subheader("🔮 Next 30 Min Forecast")

if future_level == "HIGH":
    st.error("⚠️ Expected HIGH congestion")
elif future_level == "MEDIUM":
    st.warning("⚓ Expected MEDIUM congestion")
else:
    st.success("✅ Expected LOW congestion")

# ML PREDICTION (Optional)

if os.path.exists(MODEL_PATH):

    model = joblib.load(MODEL_PATH)

    feature_dict = build_ml_features(df)
    new_features = pd.DataFrame([feature_dict])

    prediction = model.predict(new_features)[0]

    st.subheader("🔮 ML Predicted Congestion")
    st.info(f"Predicted Level: {prediction}")

else:
    st.info("ML model not found. Train and save model to enable prediction.")

st.write("Total Ships:", df["MMSI"].nunique())
st.write("Ships Near Port:", df[df["near_port"]].shape[0])

st.write("Min timestamp:", df["timestamp"].min())
st.write("Max timestamp:", df["timestamp"].max())