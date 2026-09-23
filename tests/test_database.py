from server import database as db


def metric(device_id: str, hostname: str, cpu: float = 10, memory: float = 20, disk: float = 30):
    return {
        "device_id": device_id,
        "hostname": hostname,
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
    }


def test_database_returns_latest_reading_and_devices(temporary_database):
    db.insert_metrics(metric("device-a", "alpha", cpu=25))
    db.insert_metrics(metric("device-a", "alpha", cpu=75))
    db.insert_metrics(metric("device-b", "beta"))

    latest = db.get_latest_metrics("device-a")
    devices = db.get_device_ids()

    assert latest[1] == "device-a"
    assert latest[3] == 75
    assert devices == [("device-a", "alpha"), ("device-b", "beta")]