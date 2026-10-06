from pathlib import Path

import psycopg2

from config import CRDB_NODES

SCHEMA_PATH = Path(__file__).with_name("cockroachdb_schema.sql")


def ensure_database(node: dict):
    admin_node = dict(node)
    database = admin_node["dbname"]
    admin_node["dbname"] = "defaultdb"

    with psycopg2.connect(**admin_node) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM [SHOW DATABASES] "
                "WHERE database_name = %s",
                (database,),
            )

            if cur.fetchone() is None:
                cur.execute(
                    psycopg2.sql.SQL("CREATE DATABASE {}").format(
                        psycopg2.sql.Identifier(database)
                    )
                )


def run_schema(node: dict):
    ensure_database(node)
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with psycopg2.connect(**node) as conn:
        with conn.cursor() as cur:
            cur.execute(schema)

    print("CockroachDB schema created.")


if __name__ == "__main__":
    run_schema(CRDB_NODES[0])
