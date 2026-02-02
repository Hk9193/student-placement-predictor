import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Columns that should NEVER be used for training
DROP_COLUMNS = ["Student_ID", "Name"]

def preprocess_data(df, training=True):
    """
    Preprocess data for training and inference.
    Ensures feature consistency between train and predict.
    """

    df = df.copy()

    # 
    # Target handling (training only)
    # 
    if training:
        df["Placed"] = df["Placed"].map({"Yes": 1, "No": 0})
        y = df["Placed"]
        X = df.drop(columns=["Placed"] + DROP_COLUMNS, errors="ignore")
    else:
        y = None
        X = df.drop(columns=DROP_COLUMNS, errors="ignore")

    # 
    # Ensure numeric features only
    # 
    X = X.select_dtypes(include=["int64", "float64"])

    # 
    # Scaling
    # 
    if training:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Save scaler AND column order
        joblib.dump(scaler, "scaler.pkl")
        joblib.dump(X.columns.tolist(), "features.pkl")
    else:
        scaler = joblib.load("scaler.pkl")
        trained_features = joblib.load("features.pkl")

        # Reorder columns to match training
        X = X[trained_features]
        X_scaled = scaler.transform(X)

    return X_scaled, y