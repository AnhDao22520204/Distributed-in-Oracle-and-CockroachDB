from setup import NODES, connect_to_node


def main():
    success = 0

    for idx, node in enumerate(NODES, start=1):
        conn = connect_to_node(node)
        if conn is None:
            continue

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]

            print(f"[OK] Node {idx}: {node['host']}:{node['port']}")
            print("    ", version)
            success += 1
        finally:
            conn.close()

    print(f"Connected nodes: {success}/{len(NODES)}")


if __name__ == "__main__":
    main()
