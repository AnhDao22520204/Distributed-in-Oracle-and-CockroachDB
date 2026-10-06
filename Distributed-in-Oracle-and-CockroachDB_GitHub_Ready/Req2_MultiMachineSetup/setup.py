from __future__ import annotations

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DB_USER = os.getenv("CRDB_USER", "root")
DB_PASSWORD = os.getenv("CRDB_PASSWORD", "")
DB_NAME = os.getenv("CRDB_DATABASE", "ecommerce")
DB_SSLMODE = os.getenv("CRDB_SSLMODE", "disable")


def _node(index: int) -> dict:
    return {
        "host": os.getenv(f"CRDB_NODE{index}_HOST", "127.0.0.1"),
        "port": int(os.getenv(f"CRDB_NODE{index}_PORT", "26257")),
        "user": DB_USER,
        "password": DB_PASSWORD,
        "dbname": DB_NAME,
        "sslmode": DB_SSLMODE,
        "connect_timeout": 5,
    }


NODE1 = _node(1)
NODE2 = _node(2)
NODE3 = _node(3)
NODES = [NODE1, NODE2, NODE3]

STORE_RANGES = [(1, 33), (34, 66), (67, 100)]


def connect_to_node(node_info: dict):
    """Open one CockroachDB connection or return None on connection failure."""
    try:
        return psycopg2.connect(**node_info)
    except OperationalError as exc:
        print(
            f"[ERROR] {node_info['host']}:{node_info['port']} -> {exc}"
        )
        return None


if __name__ == "__main__":
    for idx, node in enumerate(NODES, start=1):
        conn = connect_to_node(node)
        if conn is None:
            continue
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                print(f"[OK] Node {idx}: {cur.fetchone()[0]}")
        finally:
            conn.close()
