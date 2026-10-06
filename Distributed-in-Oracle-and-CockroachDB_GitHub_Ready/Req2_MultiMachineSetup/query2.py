"""Query 2: Top-selling products."""

from tabulate import tabulate

from distributed_query import query_all_partitions

QUERY = """
SELECT
    p.id AS product_id,
    p.name AS product_name,
    SUM(d.quantity) AS total_quantity,
    SUM(d.quantity * d.unit_price) AS total_revenue,
    COUNT(DISTINCT i.id) AS number_of_invoices
FROM products p
JOIN invoice_details d ON d.product_id = p.id
JOIN invoices i ON i.id = d.invoice_id
WHERE i.created_at >= CURRENT_DATE - INTERVAL '30 days'
  AND i.store_id BETWEEN %s AND %s
GROUP BY p.id, p.name
"""


def main():
    df = query_all_partitions(
        QUERY,
        [
            "product_id",
            "product_name",
            "total_quantity",
            "total_revenue",
            "number_of_invoices",
        ],
    )
    if df.empty:
        print("No data.")
        return

    df["total_quantity"] = df["total_quantity"].astype(float)
    df["total_revenue"] = df["total_revenue"].astype(float)

    result = (
        df.groupby(["product_id", "product_name"], as_index=False)
        .agg(
            total_quantity=("total_quantity", "sum"),
            total_revenue=("total_revenue", "sum"),
            number_of_invoices=("number_of_invoices", "sum"),
        )
        .sort_values("total_quantity", ascending=False)
        .head(10)
    )

    print(tabulate(result, headers="keys", tablefmt="pretty", showindex=False))


if __name__ == "__main__":
    main()
