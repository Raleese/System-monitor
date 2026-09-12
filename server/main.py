from fastapi import FastAPI
from server import database as db
from fastapi.middleware.cors import CORSMiddleware  

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
    return rows