# Requirement 4 – Oracle to CockroachDB Migration

Workflow:

```text
Oracle
  ↓ 02_dump_oracle.py
CSV
  ↓ 03_load_to_crdb.py
CockroachDB
  ↓ 05_verify.py
Validation
```

Recommended execution:

```bash
python 01_create_schema.py
python 02_dump_oracle.py
python 03_load_to_crdb.py
python 05_verify.py
```

`04_business_logic.py` demonstrates post-migration transaction retry and
inventory updates.

A real optional Airflow DAG is available under `dags/`.
