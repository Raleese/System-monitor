import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "metrics.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def create_metrics_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT NOT NULL,
            cpu REAL NOT NULL,
            memory REAL NOT NULL,
            disk REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_metrics(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO metrics (hostname, cpu, memory, disk)
        VALUES (?, ?, ?, ?)
    ''', (data["hostname"], data["cpu"], data["memory"], data["disk"]))
    conn.commit()
    conn.close()

def get_all_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM metrics ORDER BY id ASC''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_latest_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
            SELECT * 
            FROM metrics
            ORDER BY id DESC
            LIMIT 1
        ''')
    row = cursor.fetchone()
    conn.close()
    return row