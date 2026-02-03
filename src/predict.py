import pandas as pd
import joblib
import streamlit as st
from src.preprocessing import preprocess_data


# ---------------- LOAD MODEL ONCE (CACHED) ----------------
@st.cache_resource
def load_model():
    model = joblib.load("model.pkl")
    return model


def predict(input_data: dict):
    """
    Predict placement and probability
    """

    # Load model (cached)
    model = load_model()

    # Convert input dict to DataFrame
    df = pd.DataFrame([input_data])

    # Preprocess (scaling, feature order handled inside)
    X_scaled, _ = preprocess_data(df, training=False)

    # Prediction
    prediction = model.predict(X_scaled)[0]

    # Probability (safe for binary classifier)
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(X_scaled)[0][1]
    else:
        probability = 0.0  # fallback (should not happen)

    return prediction, float(probability)
