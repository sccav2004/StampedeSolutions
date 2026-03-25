import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

MODEL_PATH = "model.pkl"

def train_model(csv_file):
    df = pd.read_csv(csv_file)

    # Expect columns: diff, angle
    X = df[['diff']]
    y = df['angle']

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    return model

def load_model():
    return joblib.load(MODEL_PATH)