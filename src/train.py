import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

from preprocessing import preprocess_data

def train_model():
    df = pd.read_csv("data/student_placement_predictor_dataset.csv")

    X, y = preprocess_data(df, training=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "model.pkl")
    print("s Model saved successfully")

if __name__ == "__main__":
    train_model()