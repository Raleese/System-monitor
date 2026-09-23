from fastapi.testclient import TestClient

from server import main


client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_can_be_submitted_and_queried(temporary_database):
    payload = {
        "device_id": "device-a",
        "hostname": "alpha",
        "cpu": 42.5,
        "memory": 61.2,
        "disk": 73.8,
    }

    post_response = client.post("/metrics", json=payload)
    latest_response = client.get("/metrics/latest", params={"device_id": "device-a"})
    history_response = client.get("/metrics/history", params={"device_id": "device-a"})
    devices_response = client.get("/metrics/devices")

    assert post_response.status_code == 200
    assert post_response.json() == {"status": "metrics received"}
    assert latest_response.status_code == 200
    assert latest_response.json() == {
        "id": 1,
        "device_id": "device-a",
        "hostname": "alpha",
        "cpu": 42.5,
        "memory": 61.2,
        "disk": 73.8,
        "timestamp": latest_response.json()["timestamp"],
    }
    assert history_response.status_code == 200
    assert len(history_response.json()) == 1
    assert devices_response.json() == [{"device_id": "device-a", "hostname": "alpha"}]


def test_alerts_report_only_thresholds_exceeded(temporary_database):
    payload = {
        "device_id": "device-a",
        "hostname": "alpha",
        "cpu": 91,
        "memory": 78,
        "disk": 96,
    }

    client.post("/metrics", json=payload)
    response = client.get("/metrics/alerts", params={"device_id": "device-a"})

    assert response.status_code == 200
    alerts = response.json()
    assert [alert["metric"] for alert in alerts] == ["CPU", "Disk"]
    assert [alert["value"] for alert in alerts] == [91, 96]