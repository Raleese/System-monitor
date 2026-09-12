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
    try:
        response = requests.post("http://localhost:8000/metrics", json=metrics)
        print(f"Server response: {response.status_code}")
    except requests.RequestException as e:
        print(f"Could not reach the server: {e}")


    time.sleep(10)