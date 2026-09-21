import sqlite3
import os
from pathlib import Path

DATABASE_PATH = Path(os.getenv("MONITOR_DATABASE_PATH", str(Path(__file__).parent / "metrics.db")))
RETENTION_COUNT = int(os.getenv("MONITOR_RETENTION_COUNT", "1000"))

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def create_metrics_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            hostname TEXT NOT NULL,
            cpu REAL NOT NULL,
            memory REAL NOT NULL,
            disk REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_metrics(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO metrics (device_id, hostname, cpu, memory, disk)
        VALUES (?, ?, ?, ?, ?)
    """, (data["device_id"], data["hostname"], data["cpu"], data["memory"], data["disk"]))
    conn.commit()
    conn.close()

    delete_old_metrics(keep_count=RETENTION_COUNT)

def get_all_metrics(device_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * 
        FROM metrics 
        WHERE device_id = ?
        ORDER BY id ASC
    """, (device_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_latest_metrics(device_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT * 
            FROM metrics
            WHERE device_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (device_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_device_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT device_id, hostname
        FROM metrics
        GROUP BY device_id, hostname
        ORDER BY hostname ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_old_metrics(keep_count: int = 1000):
    conn = get_db_connection()
    cursor = conn.cursor()

    rows = get_device_ids()

    for row in rows:
        device_id = row[0]

        cursor.execute("""
            DELETE FROM metrics
            WHERE device_id = ?
            AND id NOT IN (
                SELECT id
                FROM metrics
                WHERE device_id = ?
                ORDER BY id DESC
                LIMIT ?
            )
        """, (device_id, device_id, keep_count))

    conn.commit()
    cursor.execute("VACUUM")
    conn.close()