from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = Path(__file__).resolve().parents[1]

default_args = {
    "owner": "distributed-db-team",
    "retries": 1,
}

with DAG(
    dag_id="oracle_to_cockroach_migration",
    description=(
        "Oracle export -> CockroachDB load -> verification"
    ),
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["oracle", "cockroachdb", "migration"],
) as dag:

    create_schema = BashOperator(
        task_id="create_schema",
        bash_command=(
            f"python '{PROJECT_DIR / '01_create_schema.py'}'"
        ),
    )

    dump_oracle = BashOperator(
        task_id="dump_oracle",
        bash_command=(
            f"python '{PROJECT_DIR / '02_dump_oracle.py'}'"
        ),
    )

    load_cockroachdb = BashOperator(
        task_id="load_cockroachdb",
        bash_command=(
            f"python '{PROJECT_DIR / '03_load_to_crdb.py'}'"
        ),
    )

    verify = BashOperator(
        task_id="verify_migration",
        bash_command=(
            f"python '{PROJECT_DIR / '05_verify.py'}'"
        ),
    )

    create_schema >> dump_oracle >> load_cockroachdb >> verify
