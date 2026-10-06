import csv
from pathlib import Path

import oracledb

from config import ORACLE, TABLES

OUT_DIR = Path(__file__).with_name("csv_dump")
OUT_DIR.mkdir(exist_ok=True)


def export_table(cursor, table: str, path: Path):
    cursor.execute(f"SELECT * FROM {table}")
    columns = [item[0] for item in cursor.description]

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)

        for row in cursor:
            normalized = []

            for value in row:
                if hasattr(value, "read"):
                    value = value.read()
                normalized.append(value)

            writer.writerow(normalized)

    print(f"Exported {table} -> {path}")


def main():
    with oracledb.connect(**ORACLE) as conn:
        with conn.cursor() as cursor:
            for table in TABLES:
                export_table(
                    cursor,
                    table,
                    OUT_DIR / f"{table}.csv",
                )


if __name__ == "__main__":
    main()
