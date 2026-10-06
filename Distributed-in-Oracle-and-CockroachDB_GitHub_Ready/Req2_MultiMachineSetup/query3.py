"""Query 3: Top customers by total spending."""

from tabulate import tabulate

from distributed_query import query_all_partitions

QUERY = """
SELECT
    user_id,
    store_id,
    SUM(total_amount) AS total_spent,
    COUNT(*) AS invoice_count
FROM invoices
WHERE store_id BETWEEN %s AND %s
GROUP BY user_id, store_id
HAVING SUM(total_amount) > 0
"""


def main():
    df = query_all_partitions(
        QUERY,
        ["user_id", "store_id", "total_spent", "invoice_count"],
    )
    if df.empty:
        print("No data.")
        return

    df["total_spent"] = df["total_spent"].astype(float)

    result = (
        df.groupby(["user_id", "store_id"], as_index=False)
        .agg(
            total_spent=("total_spent", "sum"),
            invoice_count=("invoice_count", "sum"),
        )
        .sort_values("total_spent", ascending=False)
        .head(20)
    )

    print(tabulate(result, headers="keys", tablefmt="pretty", showindex=False))


if __name__ == "__main__":
    main()
