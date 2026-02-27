import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st

st.header("Ship ETA Prediction")
st.info("ETA model integration coming next")

model = st.session_state.get("eta_model")

if model:
    st.success("Model loaded successfully")