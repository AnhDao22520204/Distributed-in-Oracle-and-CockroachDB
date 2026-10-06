import csv
from pathlib import Path

import psycopg2
from psycopg2 import sql

from config import CRDB_NODES, TABLES

CSV_DIR = Path(__file__).with_name("csv_dump")


def copy_csv(conn, table: str):
    path = CSV_DIR / f"{table}.csv"

    if not path.exists():
        raise FileNotFoundError(path)

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        columns = next(csv.reader(file))

    column_sql = sql.SQL(", ").join(
        sql.Identifier(column.lower())
        for column in columns
    )

    command = sql.SQL(
        "COPY {} ({}) FROM STDIN WITH CSV HEADER"
    ).format(
        sql.Identifier(table),
        column_sql,
    )

    with conn.cursor() as cur, path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        cur.copy_expert(command.as_string(conn), file)

    print(f"Loaded {table}")


def main():
    with psycopg2.connect(**CRDB_NODES[0]) as conn:
        for table in TABLES:
            copy_csv(conn, table)


if __name__ == "__main__":
    main()
