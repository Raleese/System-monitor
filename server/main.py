from fastapi import FastAPI
import database as db

app = FastAPI()
db.create_metrics_table()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/metrics")
def metrics(data: dict):
    db.insert_metrics(data)
    return {"status": "metrics received"}