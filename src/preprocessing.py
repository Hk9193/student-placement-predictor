import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

DROP_COLUMNS = ["Student_ID", "Name"]

def preprocess_data(df, training=True):
    """
    Preprocess data for training and inference.
    Ensures feature consistency between train and predict.
    """

    df = df.copy()

    # ---------------- TRAINING ----------------
    if training:
        df["Placed"] = df["Placed"].map({"Yes": 1, "No": 0})
        y = df["Placed"]

        X = df.drop(columns=["Placed"] + DROP_COLUMNS, errors="ignore")

        # Ensure numeric
        X = X.apply(pd.to_numeric, errors="coerce")

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Save artifacts
        joblib.dump(scaler, "scaler.pkl")
        joblib.dump(X.columns.tolist(), "features.pkl")

    # ---------------- INFERENCE ----------------
    else:
        y = None

        scaler = joblib.load("scaler.pkl")
        trained_features = joblib.load("features.pkl")

        X = df.drop(columns=DROP_COLUMNS, errors="ignore")

        # Ensure ALL required features exist
        for col in trained_features:
            if col not in X.columns:
                X[col] = 0  # safe default

        # Reorder columns EXACTLY
        X = X[trained_features]

        # Convert to numeric safely
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

        X_scaled = scaler.transform(X)

    return X_scaled, y
