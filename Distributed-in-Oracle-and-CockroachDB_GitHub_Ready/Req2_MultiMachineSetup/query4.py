"""Query 4: Revenue by city."""

from tabulate import tabulate

from distributed_query import query_all_partitions

QUERY = """
SELECT
    s.city,
    COUNT(DISTINCT s.id) AS store_count,
    COUNT(DISTINCT i.id) AS order_count,
    SUM(i.total_amount) AS total_revenue,
    COUNT(DISTINCT i.user_id) AS customer_count
FROM stores s
JOIN invoices i ON i.store_id = s.id
WHERE i.created_at >= CURRENT_DATE - INTERVAL '30 days'
  AND s.id BETWEEN %s AND %s
GROUP BY s.city
"""


def main():
    df = query_all_partitions(
        QUERY,
        [
            "city",
            "store_count",
            "order_count",
            "total_revenue",
            "customer_count",
        ],
    )
    if df.empty:
        print("No data.")
        return

    df["total_revenue"] = df["total_revenue"].astype(float)

    result = (
        df.groupby("city", as_index=False)
        .agg(
            store_count=("store_count", "sum"),
            order_count=("order_count", "sum"),
            total_revenue=("total_revenue", "sum"),
            customer_count=("customer_count", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
    )

    total = result["total_revenue"].sum()
    result["revenue_percentage"] = (
        100 * result["total_revenue"] / total if total else 0
    )

    print(tabulate(result, headers="keys", tablefmt="pretty", showindex=False))


if __name__ == "__main__":
    main()
