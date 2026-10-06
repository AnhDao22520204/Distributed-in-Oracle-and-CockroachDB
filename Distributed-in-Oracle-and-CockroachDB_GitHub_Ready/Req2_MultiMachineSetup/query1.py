"""Query 1: Top stores by revenue."""

from tabulate import tabulate

from distributed_query import query_all_partitions

QUERY = """
SELECT
    s.id AS store_id,
    s.name AS store_name,
    s.city,
    COUNT(DISTINCT i.id) AS invoice_count,
    SUM(i.total_amount) AS revenue,
    COUNT(DISTINCT i.user_id) AS unique_customers
FROM stores s
JOIN invoices i ON i.store_id = s.id
WHERE i.created_at >= CURRENT_DATE - INTERVAL '30 days'
  AND s.id BETWEEN %s AND %s
GROUP BY s.id, s.name, s.city
"""


def main():
    df = query_all_partitions(
        QUERY,
        [
            "store_id",
            "store_name",
            "city",
            "invoice_count",
            "revenue",
            "unique_customers",
        ],
    )
    if df.empty:
        print("No data.")
        return

    df["revenue"] = df["revenue"].astype(float)
    result = (
        df.sort_values("revenue", ascending=False)
        .drop_duplicates("store_id")
        .head(10)
    )

    print(
        tabulate(
            result.drop(columns=["_node"]),
            headers="keys",
            tablefmt="pretty",
            showindex=False,
        )
    )


if __name__ == "__main__":
    main()
