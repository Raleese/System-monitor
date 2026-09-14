# System Monitor

A small local system monitoring application. It collects CPU, memory, and disk usage from a machine, stores the readings in SQLite, and displays the latest values, recent history, and threshold alerts in a React dashboard.

## Architecture

The project has three parts:

- **Agent** (`agent/agent.py`) collects metrics with `psutil` every 10 seconds and sends them to the API.
- **Server** (`server/main.py`) provides a FastAPI API and stores metrics in `server/metrics.db`.
- **Dashboard** (`dashboard/`) is a Vite + React application that polls the API every 10 seconds.

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer and npm

## Setup

Clone the repository and open a terminal in the project root.

### 1. Install Python dependencies

Create and activate a virtual environment, then install the packages used by the server and agent:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn psutil requests
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install fastapi uvicorn psutil requests
```

### 2. Install dashboard dependencies

```bash
cd dashboard
npm install
cd ..
```

## Run the application

Open three terminals in the project root and activate the virtual environment in the terminals that run Python commands.

### Start the API server

```bash
uvicorn server.main:app --reload
```

The API is available at `http://localhost:8000`. The SQLite database is created automatically at `server/metrics.db`.

### Start the metrics agent

```bash
python agent/agent.py
```

The agent sends metrics to the API every 10 seconds. Keep this process running while using the dashboard.

### Start the dashboard

```bash
cd dashboard
npm run dev
```

Open the URL printed by Vite, usually `http://localhost:5173`.

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Returns the server health status. |
| `POST` | `/metrics` | Stores a metric reading. |
| `GET` | `/metrics/latest` | Returns the newest reading. |
| `GET` | `/metrics/history` | Returns stored readings in ascending order. |
| `GET` | `/metrics/alerts` | Returns alerts for the latest reading from each host. |

Example metric payload:

```json
{
	"hostname": "example-machine",
	"cpu": 42.5,
	"memory": 61.2,
	"disk": 73.8
}
```

## Alert thresholds and retention

The API reports an alert when a value is above one of these thresholds:

- CPU: `90%`
- Memory: `78%`
- Disk: `95%`

The database keeps the latest 1,000 metric records.

## Development commands

Run these from the `dashboard` directory:

```bash
npm run dev      # Start the development server
npm run build    # Type-check and build for production
npm run lint     # Run ESLint
npm run preview  # Preview the production build
```