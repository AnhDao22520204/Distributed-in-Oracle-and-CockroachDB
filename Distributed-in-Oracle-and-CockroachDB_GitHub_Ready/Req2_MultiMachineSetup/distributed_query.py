from __future__ import annotations

import pandas as pd

from setup import NODES, STORE_RANGES, connect_to_node


def query_all_partitions(query: str, columns: list[str]) -> pd.DataFrame:
    frames = []

    for node_index, (node, store_range) in enumerate(
        zip(NODES, STORE_RANGES), start=1
    ):
        conn = connect_to_node(node)
        if conn is None:
            continue

        start_store, end_store = store_range
        try:
            with conn.cursor() as cur:
                cur.execute(query, (start_store, end_store))
                rows = cur.fetchall()

            frame = pd.DataFrame(rows, columns=columns)
            if not frame.empty:
                frame["_node"] = node_index
                frames.append(frame)
        except Exception as exc:
            print(f"[ERROR] Node {node_index}: {exc}")
        finally:
            conn.close()

    if not frames:
        return pd.DataFrame(columns=columns)

    return pd.concat(frames, ignore_index=True)
