import argparse
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean, median

from connection import NODES, connect

DEFAULT_WORKERS = 20
DEFAULT_DURATION = 20
SUBMIT_INTERVAL = 0.01

latencies = []
node_counts = {}
lock = threading.Lock()


def worker(task_id: int):
    node_index = random.randrange(len(NODES))
    node = NODES[node_index]
    start = time.perf_counter()

    try:
        with connect(node) as conn:
            with conn.cursor() as cur:
                cur.execute("SET statement_timeout = '2000ms'")
                cur.execute(
                    """
                    UPDATE inventory
                    SET quantity = quantity + 1,
                        last_updated = now()
                    WHERE id = 1
                    """
                )
            conn.commit()
    except Exception as exc:
        print(f"[ERROR] task={task_id}, node={node_index + 1}: {exc}")
        return

    elapsed_ms = (time.perf_counter() - start) * 1000

    with lock:
        latencies.append(elapsed_ms)
        node_counts[node_index] = node_counts.get(node_index, 0) + 1


def main(workers: int, duration: int):
    global latencies, node_counts
    latencies = []
    node_counts = {}

    stop_time = time.time() + duration
    submitted = 0

    print(f"workers={workers}, duration={duration}s")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []

        while time.time() < stop_time:
            futures.append(executor.submit(worker, submitted))
            submitted += 1
            time.sleep(SUBMIT_INTERVAL)

        for future in as_completed(futures):
            future.result()

    done = len(latencies)
    if done == 0:
        print("No successful transactions.")
        return

    print("=== RESULT ===")
    print(f"Successful transactions: {done}")
    print(f"Estimated TPS: {done / duration:.2f}")
    print(f"Average latency: {mean(latencies):.2f}ms")
    print(f"Median latency: {median(latencies):.2f}ms")
    print(f"Min latency: {min(latencies):.2f}ms")
    print(f"Max latency: {max(latencies):.2f}ms")

    for index in range(len(NODES)):
        count = node_counts.get(index, 0)
        print(
            f"Node {index + 1}: {count} tx "
            f"({100 * count / done:.1f}%)"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    args = parser.parse_args()

    main(args.workers, args.duration)
