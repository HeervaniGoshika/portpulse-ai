# 🚢 Maritime Intelligence & Safety Monitoring System

An interactive maritime analytics platform that detects **port congestion**, predicts **ship ETA**, and identifies **collision risks** using AIS vessel movement data.

Built using **Python, Streamlit, and Machine Learning** with geospatial processing and real-time ship simulation.

---

## ✨ Features

- ⚓ **Port Congestion Analyzer**
  - Detect ships waiting near ports
  - Estimate congestion levels
  - Visual traffic monitoring

- 🧭 **Ship ETA Prediction**
  - Predict arrival time using speed and distance features
  - ML-based regression model

- 🚨 **Collision Risk Detection**
  - CPA / TCPA based collision analysis
  - Velocity vector computation
  - Real-time alert generation

- 🌍 **Live Ship Visualization**
  - Interactive Pydeck map
  - Time-based ship movement simulation
  - Vessel information tooltips

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas & NumPy
- Scikit-learn
- Pydeck
- SciPy (KDTree)
- Haversine

---

## 📁 Project Structure

marine-intelligence-system/
│
├── data/
├── src/
├── streamlit_app/
├── models/
├── notebooks/
└── utils/

---

## ▶️ Run the App

```bash
pip install -r requirements.txt
streamlit run streamlit_app/app.py