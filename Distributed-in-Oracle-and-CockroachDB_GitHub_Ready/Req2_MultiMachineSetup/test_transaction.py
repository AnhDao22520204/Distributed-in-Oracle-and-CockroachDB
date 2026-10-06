from transaction_manager import run_transaction_with_retry


def read_cluster_time(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT now()")
        return cur.fetchone()[0]


if __name__ == "__main__":
    cluster_time = run_transaction_with_retry(read_cluster_time)
    print("Transaction completed:", cluster_time)
