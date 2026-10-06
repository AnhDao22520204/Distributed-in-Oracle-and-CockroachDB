import oracledb
import psycopg2
from psycopg2 import sql

from config import CRDB_NODES, ORACLE, TABLES


def oracle_count(cursor, table: str):
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    return int(cursor.fetchone()[0])


def crdb_count(conn, table: str):
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("SELECT COUNT(*) FROM {}").format(
                sql.Identifier(table)
            )
        )
        return int(cur.fetchone()[0])


def main():
    mismatches = []

    with oracledb.connect(**ORACLE) as oracle_conn, \
            psycopg2.connect(**CRDB_NODES[0]) as crdb_conn:

        with oracle_conn.cursor() as oracle_cur:
            print(
                f"{'Table':<20}"
                f"{'Oracle':>15}"
                f"{'CockroachDB':>15}"
                f"{'Status':>12}"
            )
            print("-" * 62)

            for table in TABLES:
                source = oracle_count(oracle_cur, table)
                target = crdb_count(crdb_conn, table)
                status = "OK" if source == target else "MISMATCH"

                if status != "OK":
                    mismatches.append(table)

                print(
                    f"{table:<20}"
                    f"{source:>15,}"
                    f"{target:>15,}"
                    f"{status:>12}"
                )

    if mismatches:
        raise SystemExit(
            "Row-count mismatch: " + ", ".join(mismatches)
        )

    print("Verification successful.")


if __name__ == "__main__":
    main()
