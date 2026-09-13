from fastapi import FastAPI
from server import database as db
from fastapi.middleware.cors import CORSMiddleware  

cpu_threshold = 90.0
mem_threshold = 78.0
disk_threshold = 95.0

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
def metrics_latest():
    row = db.get_latest_metrics()

    if row is None:
        return None

    return {
        "id": row[0],
        "hostname": row[1],
        "cpu": row[2],
        "memory": row[3],
        "disk": row[4],
        "timestamp": row[5]
    }

@app.get("/metrics/history")
def metrics_history():
    rows = db.get_all_metrics()
    return [
        {
            "id": row[0],
            "hostname": row[1],
            "cpu": row[2],
            "memory": row[3],
            "disk": row[4],
            "timestamp": row[5]
        }
        for row in rows
    ]

@app.get("/metrics/alerts")
def metrics_alerts():
    rows = db.get_all_metrics()
    latest_by_hostname = {}
    for row in rows:
        latest_by_hostname[row[1]] = row

    alerts = []
    for row in latest_by_hostname.values():
        if row[2] > cpu_threshold:
            alerts.append({"id": row[0], "hostname": row[1], "metric": "CPU", "value": row[2], "timestamp": row[5]})
        if row[3] > mem_threshold:
            alerts.append({"id": row[0], "hostname": row[1], "metric": "Memory", "value": row[3], "timestamp": row[5]})
        if row[4] > disk_threshold:
            alerts.append({"id": row[0], "hostname": row[1], "metric": "Disk", "value": row[4], "timestamp": row[5]})
    return alerts