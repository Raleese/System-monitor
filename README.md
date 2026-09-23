# System Monitor

A small system monitoring application that collects CPU, memory, and disk usage, stores readings in SQLite, and displays the latest values, history, and threshold alerts in a React dashboard.

## Demonstration

<img width="1916" height="1062" alt="Recording 2026-09-23 134606" src="https://github.com/user-attachments/assets/8fe7c4ca-5b3c-498e-b64a-13c325328715" />

## Architecture

The project has three parts:

- **Agent** (`agent/agent.py`) collects metrics with `psutil` every 10 seconds and sends them to the API.
- **Server** (`server/main.py`) provides the FastAPI API and stores metrics in SQLite.
- **Dashboard** (`dashboard/`) is a React and Vite application that polls the API every 10 seconds.

The repository also includes Docker support.

## Requirements

For local development:

- Python 3.10 or newer
- Node.js 18 or newer and npm

For Docker:

- Docker Desktop with the Linux container engine running

For tests:

```powershell
pip install -r requirements-dev.txt
```

## Quick Start With Docker

From the repository root, build and start the API and dashboard:

```powershell
docker compose up --build
```

Open the dashboard at `http://localhost:5173`.

The API is available at `http://localhost:8000`, and its health endpoint is:

```text
http://localhost:8000/health
```

To stop the services:

```powershell
docker compose down
```

To stop the services and delete the stored SQLite data:

```powershell
docker compose down -v
```

### Run an agent on a monitored device

Keep the API and dashboard running on the server machine, then install and run the agent directly on every device that should be monitored. On the server machine itself:

```powershell
docker compose up --build -d
$env:MONITOR_SERVER_URL = "http://localhost:8000"
python agent/agent.py
```

On another device, set the URL to the server machine's LAN address. For example:

```bash
MONITOR_SERVER_URL=http://192.168.1.20:8000 python agent/agent.py
```

On Windows PowerShell:

```powershell
$env:MONITOR_SERVER_URL = "http://192.168.1.20:8000"
python agent/agent.py
```

The API must be reachable from each monitored device on port `8000`. If the API runs on another machine, start it with Docker as usual and allow port `8000` through that machine's firewall.

## Configuration

The application uses environment variables with local defaults.

### Server variables

| Variable | Default | Description |
| --- | --- | --- |
| `MONITOR_DATABASE_PATH` | `server/metrics.db` | SQLite database path outside Docker. Compose sets it to `/data/metrics.db`. |
| `MONITOR_ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated dashboard origins allowed by CORS. |
| `MONITOR_CPU_THRESHOLD` | `90` | CPU alert threshold as a percentage. |
| `MONITOR_MEMORY_THRESHOLD` | `78` | Memory alert threshold as a percentage. |
| `MONITOR_DISK_THRESHOLD` | `95` | Disk alert threshold as a percentage. |
| `MONITOR_RETENTION_COUNT` | `1000` | Number of readings retained per device. |

### Agent variables

| Variable | Default | Description |
| --- | --- | --- |
| `MONITOR_SERVER_URL` | `http://127.0.0.1:8000` | API URL used by the agent. Set it to the server machine's LAN address on remote devices. |
| `MONITOR_COLLECTION_INTERVAL` | `10` | Seconds between metric submissions. |
| `MONITOR_DEVICE_ID_FILE` | `agent/.device_id` | File used to persist the agent's device ID. |

### Dashboard variable

| Variable | Default | Description |
| --- | --- | --- |
| `VITE_API_URL` | `http://127.0.0.1:8000` | API URL embedded into the frontend during the Vite build. |

For Docker builds, pass it as a build argument. The browser must be able to resolve the URL; Docker service names such as `server` are only resolvable from other containers.

## Persistence and Device IDs

The server creates the SQLite database automatically. In Docker, the database is stored in the named `metrics-data` volume so it survives container recreation.

Each agent generates a UUID the first time it runs and stores it in `.device_id`. When the agent runs directly on a device, keep that file so the device keeps the same identity between runs. Delete the file only when you intentionally want the device to appear as a new device.

```powershell
Remove-Item agent\.device_id
```

Every monitored device should run one host agent. The dashboard identifies devices using each agent's hostname and persistent device ID.

## Alerts and Retention

The API reports an alert when a value is above these thresholds:

- CPU: `90%`
- Memory: `78%`
- Disk: `95%`

The default retention limit is 1,000 readings per device.

## Tests

Run the API and database tests from the repository root:

```powershell
python -m pytest tests -q
```

The tests use temporary SQLite databases, so they do not modify the development database.

## Troubleshooting

### Docker cannot connect to the Docker API

Start Docker Desktop and make sure its Linux container engine is running, then retry:

```powershell
docker compose up --build
```

### Dashboard cannot load devices

Check that the API is running at `http://localhost:8000/health`, that the dashboard was built with the correct `VITE_API_URL`, and that the API's `MONITOR_ALLOWED_ORIGINS` includes the dashboard URL.

### The dashboard shows the wrong device

Run `python agent/agent.py` directly on the monitored device. Do not use a containerized agent for this use case, because it reports the container's identity and resource environment instead of the physical device.

### A remote device cannot send metrics

Set `MONITOR_SERVER_URL` to the API host's LAN address, verify that the device can reach port `8000`, and allow inbound TCP port `8000` through the API host's firewall. Do not use `localhost` on a remote device; it points back to that device itself.

### Port already in use

Change the host side of the port mapping in `docker-compose.yml`. For example, change `5173:80` to `8080:80`, then also add `http://localhost:8080` to `MONITOR_ALLOWED_ORIGINS`.
