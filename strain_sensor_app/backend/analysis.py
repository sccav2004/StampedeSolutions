import pandas as pd
from calibration import load_model

def process_data(file):
    df = pd.read_csv(file)
    df.columns = ["time", "diff", "med", "lat"]

    model = load_model()

    df["angle"] = model.predict(df[['diff']])

    # Trend
    df["rolling_mean"] = df["angle"].rolling(10).mean()
    df["trend"] = df["rolling_mean"].diff()

    return df