import time
import psutil
import socket

metrics = {
    "hostname": socket.gethostname(),
    "cpu": psutil.cpu_percent(interval=1),
    "memory": psutil.virtual_memory().percent,
    "disk": psutil.disk_usage("/").percent
}

while True:

    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory.percent}%")
    print(f"Disk Usage: {disk.percent}%")
    print("-" * 30);

    time.sleep(10)