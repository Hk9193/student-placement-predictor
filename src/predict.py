import pandas as pd
import joblib
from src.preprocessing import preprocess_data

def predict(input_data: dict):
    model = joblib.load("model.pkl")

    df = pd.DataFrame([input_data])
    X_scaled, _ = preprocess_data(df, training=False)

    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][1]

    return prediction, probability