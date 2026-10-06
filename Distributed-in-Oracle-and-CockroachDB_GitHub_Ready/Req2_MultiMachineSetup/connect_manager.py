import threading

from setup import NODES, connect_to_node

_lock = threading.Lock()
_current_idx = 0


def get_next_node():
    global _current_idx
    with _lock:
        node = NODES[_current_idx]
        _current_idx = (_current_idx + 1) % len(NODES)
    return node


def connect_with_failover():
    for node in NODES:
        conn = connect_to_node(node)
        if conn is not None:
            return conn
    return None


def connect_with_load_balancing():
    for _ in range(len(NODES)):
        conn = connect_to_node(get_next_node())
        if conn is not None:
            return conn
    return None
