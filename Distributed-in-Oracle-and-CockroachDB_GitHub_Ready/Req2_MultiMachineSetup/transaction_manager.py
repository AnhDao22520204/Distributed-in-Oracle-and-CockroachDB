import random
import time

from psycopg2 import DatabaseError, OperationalError
from psycopg2.errors import SerializationFailure

from setup import NODES, connect_to_node

MAX_RETRIES = 5


def _connect_any():
    for node in NODES:
        conn = connect_to_node(node)
        if conn is not None:
            return conn
    return None


def run_transaction_with_retry(txn_fn, max_retries: int = MAX_RETRIES):
    last_error = None

    for attempt in range(1, max_retries + 1):
        conn = _connect_any()
        if conn is None:
            last_error = RuntimeError("No node is reachable.")
        else:
            try:
                conn.autocommit = False
                result = txn_fn(conn)
                conn.commit()
                return result
            except SerializationFailure as exc:
                conn.rollback()
                last_error = exc
                print(f"[RETRY {attempt}] SerializationFailure: {exc}")
            except OperationalError as exc:
                conn.rollback()
                last_error = exc
                print(f"[RETRY {attempt}] OperationalError: {exc}")
            except DatabaseError:
                conn.rollback()
                raise
            finally:
                conn.close()

        if attempt < max_retries:
            time.sleep(random.uniform(0.2, 1.0))

    raise RuntimeError(
        f"Transaction failed after {max_retries} attempts: {last_error}"
    )
