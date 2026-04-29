import pandas as pd

SLOPE = 0.0176
INTERCEPT = -0.0723

MIN_ANGLE = 0.0
MAX_ANGLE = 12.0

def process_data(file):
    df = pd.read_csv(file)
    df.columns = ["time", "diff", "med", "lat"]

    df["angle"] = df["diff"] / SLOPE + INTERCEPT
    df["angle"] = df["angle"].clip(lower=MIN_ANGLE, upper=MAX_ANGLE)

    df["rolling_mean"] = df["angle"].rolling(window=10, min_periods=1).mean()
    df["trend"] = df["rolling_mean"].diff().fillna(0)

    return df
