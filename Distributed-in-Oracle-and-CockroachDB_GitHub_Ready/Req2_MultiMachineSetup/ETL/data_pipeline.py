from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

HOST = os.getenv("CRDB_NODE1_HOST", "127.0.0.1")
PORT = int(os.getenv("CRDB_NODE1_PORT", "26257"))
USER = os.getenv("CRDB_USER", "root")
PASSWORD = os.getenv("CRDB_PASSWORD", "")
DATABASE = os.getenv("CRDB_DATABASE", "ecommerce")
SSLMODE = os.getenv("CRDB_SSLMODE", "disable")

auth = USER if not PASSWORD else f"{USER}:{PASSWORD}"
DATABASE_URL = (
    f"cockroachdb://{auth}@{HOST}:{PORT}/{DATABASE}"
    f"?sslmode={SSLMODE}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def read_data_for_date(target_date: str) -> pd.DataFrame:
    statement = text("""
        SELECT id, user_id, store_id, total_amount, created_at
        FROM invoices
        WHERE CAST(created_at AS DATE) = :target_date
        ORDER BY id
    """)

    try:
        return pd.read_sql_query(
            statement,
            engine,
            params={"target_date": target_date},
            parse_dates=["created_at"],
        )
    except Exception as exc:
        print("Read failed:", exc)
        return pd.DataFrame()


def analyze_revenue_by_store(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=["store_id", "invoice_count", "total_revenue"]
        )

    work = df.copy()
    work["total_amount"] = pd.to_numeric(work["total_amount"])

    return (
        work.groupby("store_id", as_index=False)
        .agg(
            invoice_count=("id", "count"),
            total_revenue=("total_amount", "sum"),
        )
    )


def compute_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    values = pd.to_numeric(df["total_amount"]).to_numpy(dtype=float)

    return {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
    }


def ensure_daily_reports_table():
    ddl = text("""
        CREATE TABLE IF NOT EXISTS daily_reports (
            report_date DATE NOT NULL,
            store_id INT NOT NULL,
            invoice_count INT NOT NULL,
            total_revenue DECIMAL(18,2) NOT NULL,
            created_at TIMESTAMP DEFAULT now(),
            PRIMARY KEY (report_date, store_id)
        )
    """)

    with engine.begin() as conn:
        conn.execute(ddl)


def write_daily_report(report_date: str, summary: pd.DataFrame):
    ensure_daily_reports_table()

    if summary.empty:
        return

    statement = text("""
        INSERT INTO daily_reports
            (report_date, store_id, invoice_count, total_revenue)
        VALUES
            (:report_date, :store_id, :invoice_count, :total_revenue)
        ON CONFLICT (report_date, store_id)
        DO UPDATE SET
            invoice_count = excluded.invoice_count,
            total_revenue = excluded.total_revenue,
            created_at = now()
    """)

    with engine.begin() as conn:
        for row in summary.to_dict(orient="records"):
            conn.execute(
                statement,
                {
                    "report_date": report_date,
                    "store_id": int(row["store_id"]),
                    "invoice_count": int(row["invoice_count"]),
                    "total_revenue": float(row["total_revenue"]),
                },
            )
