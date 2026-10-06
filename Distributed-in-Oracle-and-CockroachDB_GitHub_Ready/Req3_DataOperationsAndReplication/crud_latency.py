import random
import string
import time
from statistics import mean

from connection import NODES, connect

LOOPS = 50
OPS = ["INSERT", "SELECT", "UPDATE", "DELETE"]


def benchmark_node(node: dict, loops: int = LOOPS):
    results = {op: [] for op in OPS}

    with connect(node) as conn:
        with conn.cursor() as cur:
            for _ in range(loops):
                row_id = random.randint(2_000_000_000, 2_100_000_000)
                name = "bench-" + "".join(
                    random.choices(string.ascii_lowercase, k=8)
                )
                price = random.randint(10, 2000)
                store_id = random.randint(1, 100)

                start = time.perf_counter()
                cur.execute(
                    """
                    INSERT INTO products (id, name, price, store_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (row_id, name, price, store_id),
                )
                conn.commit()
                results["INSERT"].append(
                    (time.perf_counter() - start) * 1000
                )

                start = time.perf_counter()
                cur.execute(
                    "SELECT * FROM products WHERE id = %s",
                    (row_id,),
                )
                cur.fetchone()
                results["SELECT"].append(
                    (time.perf_counter() - start) * 1000
                )

                start = time.perf_counter()
                cur.execute(
                    "UPDATE products SET price = price + 1 WHERE id = %s",
                    (row_id,),
                )
                conn.commit()
                results["UPDATE"].append(
                    (time.perf_counter() - start) * 1000
                )

                start = time.perf_counter()
                cur.execute(
                    "DELETE FROM products WHERE id = %s",
                    (row_id,),
                )
                conn.commit()
                results["DELETE"].append(
                    (time.perf_counter() - start) * 1000
                )

    return {op: mean(values) for op, values in results.items()}


def main():
    for idx, node in enumerate(NODES, start=1):
        try:
            result = benchmark_node(node)
            metrics = " | ".join(
                f"{op}={result[op]:.2f}ms" for op in OPS
            )
            print(
                f"Node {idx} {node['host']}:{node['port']} | {metrics}"
            )
        except Exception as exc:
            print(f"Node {idx} failed: {exc}")


if __name__ == "__main__":
    main()
