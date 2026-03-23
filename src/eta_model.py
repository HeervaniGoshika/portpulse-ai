import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from src.congestion_model import compute_congestion_features, congestion_severity

def adjust_eta_with_congestion(eta_hours, severity):

    # severity score 0–100
    delay = severity * 0.02

    return eta_hours + delay

def train_eta_model(X, y):
    model = RandomForestRegressor()
    model.fit(X, y)
    return model

def create_eta_model():

    model = LinearRegression()

    return model


