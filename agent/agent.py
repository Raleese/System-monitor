import time
import psutil
import socket
import requests

while True:
    metrics = {
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent
    }
    requests.post("http://localhost:8000/metrics", json=metrics)
    time.sleep(10)