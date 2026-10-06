from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DB_USER = os.getenv("CRDB_USER", "root")
DB_PASSWORD = os.getenv("CRDB_PASSWORD", "")
DB_NAME = os.getenv("CRDB_DATABASE", "ecommerce")
DB_SSLMODE = os.getenv("CRDB_SSLMODE", "disable")

NODES = [
    {
        "host": os.getenv(f"CRDB_NODE{i}_HOST", "127.0.0.1"),
        "port": int(os.getenv(f"CRDB_NODE{i}_PORT", "26257")),
    }
    for i in (1, 2, 3)
]


@contextmanager
def connect(node: dict):
    conn = psycopg2.connect(
        host=node["host"],
        port=node["port"],
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        sslmode=DB_SSLMODE,
        connect_timeout=5,
    )

    try:
        yield conn
    finally:
        conn.close()
