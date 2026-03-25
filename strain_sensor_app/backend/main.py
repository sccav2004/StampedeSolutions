from fastapi import FastAPI
from database import Base, engine
from serial_reader import download_from_device
from analysis import process_data

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/download")
def download(port: str):
    df = download_from_device(port)
    df, r2, adj_r2 = process_data(df)

    return {
        "data": df.to_dict(),
        "r2": r2,
        "adj_r2": adj_r2
    }