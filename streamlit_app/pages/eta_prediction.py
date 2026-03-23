import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import streamlit as st
import joblib
import datetime


from src.data_loader import load_ais_data
from src.feature_engineering import add_velocity, add_port_geofence, add_waiting_time, add_eta_features
from src.eta_model import adjust_eta_with_congestion
from src.congestion_model import compute_congestion_features, congestion_severity


PORT_LAT = 17.6868
PORT_LON = 83.2185

st.title("⏱ Ship ETA Prediction")

model = joblib.load("models/eta_model.pkl")

df = load_ais_data("data/processed/raw.csv")

df = add_velocity(df)
df = add_port_geofence(df, PORT_LAT, PORT_LON)
df = add_waiting_time(df)

# compute congestion
ships_near, waiting_ships, avg_wait = compute_congestion_features(df)
congestion_score = congestion_severity(ships_near, waiting_ships, avg_wait)

df = add_eta_features(df, congestion_score)

ship = st.selectbox("Select Ship", df["MMSI"].unique())

model = joblib.load("models/eta_model.pkl")

ship_data = df.iloc[-1]

X = [[
    ship_data["distance_to_port"],
    ship_data["speed"],
    ship_data["traffic_density"],
    ship_data["heading"],
    ship_data["vessel_type_cargo"],
    ship_data["vessel_type_tanker"],
    ship_data["vessel_type_container"]
]]

eta = model.predict(X)[0]

st.metric("Predicted ETA (minutes)", round(eta,2))

ships_near, waiting_ships, avg_wait = compute_congestion_features(df)

severity = congestion_severity(ships_near, waiting_ships, avg_wait)

# predicted ETA in hours
eta_hours = model.predict(X)[0]

arrival_time = datetime.datetime.now() + datetime.timedelta(hours=eta_hours)

st.metric("Predicted ETA (hours)", round(eta_hours, 2))

st.write("Estimated Arrival Time:", arrival_time.strftime("%Y-%m-%d %H:%M:%S"))





adjusted_eta = adjust_eta_with_congestion(eta, severity)

st.metric("Adjusted ETA (hours)", round(adjusted_eta, 2))
