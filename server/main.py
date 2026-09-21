import os

from fastapi import FastAPI
from server import database as db
from fastapi.middleware.cors import CORSMiddleware  

cpu_threshold = float(os.getenv("MONITOR_CPU_THRESHOLD", "90"))
mem_threshold = float(os.getenv("MONITOR_MEMORY_THRESHOLD", "78"))
disk_threshold = float(os.getenv("MONITOR_DISK_THRESHOLD", "95"))
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "MONITOR_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db.create_metrics_table()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/metrics")
def metrics(data: dict):
    db.insert_metrics(data)
    return {"status": "metrics received"}

@app.get("/metrics/latest")
def metrics_latest(device_id: str):
    row = db.get_latest_metrics(device_id)

    if row is None:
        return None

    return {
        "id": row[0],
        "device_id": row[1],
        "hostname": row[2],
        "cpu": row[3],
        "memory": row[4],
        "disk": row[5],
        "timestamp": row[6]
    }

@app.get("/metrics/history")
def metrics_history(device_id: str):
    rows = db.get_all_metrics(device_id)
    return [
        {
            "id": row[0],
            "device_id": row[1],
            "hostname": row[2],
            "cpu": row[3],
            "memory": row[4],
            "disk": row[5],
            "timestamp": row[6]
        }
        for row in rows
    ]

@app.get("/metrics/devices")
def metrics_devices():
    rows = db.get_device_ids()

    return [{
        "device_id": row[0],
        "hostname": row[1]
    } for row in rows]

@app.get("/metrics/alerts")
def metrics_alerts(device_id: str):
    rows = db.get_all_metrics(device_id)
    latest = rows[-1] if rows else None
    if latest is None:
        return []

    alerts = []
    if latest[3] > cpu_threshold:
        alerts.append({"id": latest[0], "device_id": latest[1], "hostname": latest[2], "metric": "CPU", "value": latest[3], "timestamp": latest[6]})
    if latest[4] > mem_threshold:
        alerts.append({"id": latest[0], "device_id": latest[1], "hostname": latest[2], "metric": "Memory", "value": latest[4], "timestamp": latest[6]})
    if latest[5] > disk_threshold:
        alerts.append({"id": latest[0], "device_id": latest[1], "hostname": latest[2], "metric": "Disk", "value": latest[5], "timestamp": latest[6]})
    return alerts