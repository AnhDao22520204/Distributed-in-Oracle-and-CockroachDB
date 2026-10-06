import random
import time

import psycopg2
from psycopg2 import DatabaseError, OperationalError
from psycopg2.errors import SerializationFailure

from config import CRDB_NODES

MAX_RETRIES = 5


def run_txn(work, max_retries: int = MAX_RETRIES):
    last_error = None

    for attempt in range(1, max_retries + 1):
        for node in CRDB_NODES:
            try:
                with psycopg2.connect(**node) as conn:
                    with conn.cursor() as cur:
                        result = work(cur)
                    conn.commit()
                    return result

            except SerializationFailure as exc:
                last_error = exc
                print(
                    f"[RETRY {attempt}] "
                    f"SerializationFailure: {exc}"
                )
                break

            except OperationalError as exc:
                last_error = exc
                print(
                    f"[FAILOVER] "
                    f"{node['host']}:{node['port']} -> {exc}"
                )
                continue

            except DatabaseError:
                raise

        if attempt < max_retries:
            time.sleep(random.uniform(0.2, 1.0))

    raise RuntimeError(f"Transaction failed: {last_error}")


def create_invoice(
    store_id: int,
    customer_id: int,
    employee_id: int,
    items,
):
    """
    items = [(product_id, quantity, unit_price), ...]

    Inventory is updated for every item inside the loop.
    """

    def work(cur):
        total = sum(
            quantity * unit_price
            for _, quantity, unit_price in items
        )

        cur.execute(
            """
            INSERT INTO invoice
                (
                    store_id,
                    customer_id,
                    employee_id,
                    total_amount
                )
            VALUES (%s, %s, %s, %s)
            RETURNING invoice_id
            """,
            (store_id, customer_id, employee_id, total),
        )

        invoice_id = cur.fetchone()[0]

        for product_id, quantity, unit_price in items:
            cur.execute(
                """
                INSERT INTO invoice_detail
                    (
                        invoice_id,
                        product_id,
                        quantity,
                        unit_price
                    )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    invoice_id,
                    product_id,
                    quantity,
                    unit_price,
                ),
            )

            cur.execute(
                """
                UPDATE inventory
                   SET quantity = quantity - %s,
                       last_updated = now()
                 WHERE store_id = %s
                   AND product_id = %s
                   AND quantity >= %s
                RETURNING quantity
                """,
                (
                    quantity,
                    store_id,
                    product_id,
                    quantity,
                ),
            )

            if cur.fetchone() is None:
                raise ValueError(
                    f"Insufficient inventory for "
                    f"product {product_id}"
                )

        return invoice_id

    return run_txn(work)


if __name__ == "__main__":
    new_invoice_id = create_invoice(
        store_id=1,
        customer_id=101,
        employee_id=501,
        items=[(301, 2, 19.99)],
    )

    print("New invoice:", new_invoice_id)
