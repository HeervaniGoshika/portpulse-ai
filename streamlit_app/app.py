import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import streamlit as st
import joblib

# MUST be first Streamlit command
st.set_page_config(page_title="Maritime Intelligence", layout="wide")

st.title("🚢 Maritime Intelligence System")
st.markdown("Use the sidebar to navigate.")

# -------- Metrics --------
c1, c2, c3 = st.columns(3)

c1.metric("Ships Near Port", 42)
c2.metric("Waiting Ships", 12)
c3.metric("Collision Alerts", 3)

st.divider()

# -------- Alerts --------
st.error("⚠️ Collision risk detected")
st.warning("🚢 Congestion increasing")
st.success("✅ Normal traffic")

# -------- Sidebar --------
with st.sidebar:
    st.title("Navigation")
    st.info("Maritime Intelligence System")

# -------- Model Loading (SAFE) --------
@st.cache_resource
def load_models():
    model_path = os.path.join(PROJECT_ROOT, "models", "eta_model.pkl")

    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

eta_model = load_models()

if eta_model:
    st.session_state["eta_model"] = eta_model
else:
    st.warning("ETA model not trained yet")

st.write("Use sidebar to navigate")