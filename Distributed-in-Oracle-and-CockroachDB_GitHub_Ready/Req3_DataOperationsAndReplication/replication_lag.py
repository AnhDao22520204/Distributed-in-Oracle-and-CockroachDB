import argparse
import time

from connection import NODES, connect


def measure_visibility(timeout_seconds: float = 15.0):
    if len(NODES) < 2:
        raise RuntimeError("At least two nodes are required.")

    row_id = int(time.time() * 1_000_000)

    with connect(NODES[0]) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO payments
                    (id, invoice_id, amount, status)
                VALUES (%s, %s, %s, %s)
                """,
                (row_id, 1, 0.01, "completed"),
            )
        conn.commit()

    start = time.perf_counter()
    polls = 0

    while time.perf_counter() - start < timeout_seconds:
        polls += 1

        try:
            with connect(NODES[1]) as conn:
                conn.autocommit = True

                with conn.cursor() as cur:
                    cur.execute(
                        """
                        BEGIN TRANSACTION
                        AS OF SYSTEM TIME follower_read_timestamp()
                        """
                    )
                    cur.execute(
                        "SELECT id FROM payments WHERE id = %s",
                        (row_id,),
                    )
                    result = cur.fetchone()
                    cur.execute("COMMIT")

            if result:
                elapsed_ms = (time.perf_counter() - start) * 1000
                print(
                    f"Follower-read visibility delay: "
                    f"{elapsed_ms:.1f}ms"
                )
                print(f"Polling count: {polls}")
                print(f"Marker row ID: {row_id}")
                return elapsed_ms

        except Exception as exc:
            print(f"[POLL ERROR] {exc}")

        time.sleep(0.05)

    raise TimeoutError(
        f"Marker {row_id} not visible after {timeout_seconds}s"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()

    measure_visibility(args.timeout)
