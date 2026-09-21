import time
import psutil
import socket
import requests
import os
import uuid
from pathlib import Path

SERVER_URL = os.getenv("MONITOR_SERVER_URL", "http://127.0.0.1:8000").rstrip("/")
COLLECTION_INTERVAL = float(os.getenv("MONITOR_COLLECTION_INTERVAL", "10"))
DEVICE_ID_FILE = Path(__file__).with_name(".device_id")

def get_device_id() -> str:
    if DEVICE_ID_FILE.exists():
        return DEVICE_ID_FILE.read_text().strip()
    else:
        device_id = str(uuid.uuid4())
        DEVICE_ID_FILE.write_text(device_id)
        return device_id

device_id = get_device_id()

while True:
    metrics = {
        "device_id": device_id,
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage(Path.home().anchor).percent
    }
    try:
        response = requests.post(SERVER_URL + "/metrics", json=metrics)
        print(f"Server response: {response.status_code}")
    except requests.RequestException as e:
        print(f"Could not reach the server: {e}")


    time.sleep(COLLECTION_INTERVAL)