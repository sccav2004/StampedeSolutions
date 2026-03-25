import serial
import pandas as pd

def download_from_device(port):
    ser = serial.Serial(port, 115200, timeout=5)
    ser.write(b"DOWNLOAD\n")

    lines = []
    while True:
        line = ser.readline().decode().strip()
        if not line:
            break
        lines.append(line)

    ser.close()

    df = pd.DataFrame(
        [l.split(",") for l in lines],
        columns=["timestamp", "voltage"]
    )

    df["timestamp"] = df["timestamp"].astype(float)
    df["voltage"] = df["voltage"].astype(float)

    return df