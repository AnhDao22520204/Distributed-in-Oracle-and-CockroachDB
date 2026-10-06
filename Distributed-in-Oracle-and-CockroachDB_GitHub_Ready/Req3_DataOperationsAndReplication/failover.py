import argparse
import time

from connection import NODES, connect


def wait_for_cluster(stopped_index: int, timeout: float = 30.0):
    start = time.perf_counter()
    attempts = 0

    while time.perf_counter() - start < timeout:
        attempts += 1

        for index, node in enumerate(NODES):
            if index == stopped_index:
                continue

            try:
                with connect(node) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT 1")
                        cur.fetchone()

                downtime = time.perf_counter() - start
                print(
                    f"Cluster reachable via node {index + 1} "
                    f"after {downtime:.2f}s "
                    f"({attempts} attempts)."
                )
                return downtime

            except Exception:
                pass

        time.sleep(0.1)

    raise TimeoutError(
        f"Cluster did not become reachable within {timeout}s."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Stop one CockroachDB node manually, then run this script "
            "to measure client-observed recovery."
        )
    )
    parser.add_argument(
        "--stopped-node",
        type=int,
        default=1,
        choices=range(1, len(NODES) + 1),
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    print(
        f"Assuming node {args.stopped_node} is stopped. "
        "Polling remaining nodes..."
    )
    wait_for_cluster(args.stopped_node - 1, args.timeout)
