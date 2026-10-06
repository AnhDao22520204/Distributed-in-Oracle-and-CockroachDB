from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

ORACLE = {
    "user": os.getenv("ORACLE_USER", "C##CN1"),
    "password": os.getenv("ORACLE_PASSWORD", ""),
    "dsn": os.getenv("ORACLE_DSN", "127.0.0.1:1521/ORCL"),
}

CRDB_NODES = [
    {
        "host": os.getenv(f"CRDB_NODE{i}_HOST", "127.0.0.1"),
        "port": int(os.getenv(f"CRDB_NODE{i}_PORT", "26257")),
        "user": os.getenv("CRDB_USER", "root"),
        "password": os.getenv("CRDB_PASSWORD", ""),
        "dbname": os.getenv("CRDB_DATABASE", "ecommerce"),
        "sslmode": os.getenv("CRDB_SSLMODE", "disable"),
        "connect_timeout": 5,
    }
    for i in (1, 2, 3)
]

TABLES = [
    "stores",
    "category",
    "supplier",
    "product_base",
    "product_extra",
    "customer_base",
    "customer_extra",
    "employee",
    "inventory",
    "invoice",
    "invoice_detail",
    "salary",
    "payment",
]
