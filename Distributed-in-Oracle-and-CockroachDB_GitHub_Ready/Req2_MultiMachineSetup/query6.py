"""Query 6: Shopping trend analysis by hour, weekday and month."""

import pandas as pd
from tabulate import tabulate

from distributed_query import query_all_partitions

QUERY = """
SELECT
    EXTRACT(HOUR FROM created_at) AS hour_of_day,
    EXTRACT(DOW FROM created_at) AS day_of_week,
    EXTRACT(MONTH FROM created_at) AS month,
    COUNT(DISTINCT id) AS order_count,
    SUM(total_amount) AS revenue,
    COUNT(DISTINCT user_id) AS customer_count
FROM invoices
WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
  AND store_id BETWEEN %s AND %s
GROUP BY
    EXTRACT(HOUR FROM created_at),
    EXTRACT(DOW FROM created_at),
    EXTRACT(MONTH FROM created_at)
"""


def main():
    df = query_all_partitions(
        QUERY,
        [
            "hour_of_day",
            "day_of_week",
            "month",
            "order_count",
            "revenue",
            "customer_count",
        ],
    )
    if df.empty:
        print("No data.")
        return

    for col in [
        "hour_of_day",
        "day_of_week",
        "month",
        "order_count",
        "revenue",
        "customer_count",
    ]:
        df[col] = pd.to_numeric(df[col])

    hourly = (
        df.groupby("hour_of_day", as_index=False)
        .agg(order_count=("order_count", "sum"), revenue=("revenue", "sum"))
        .sort_values("order_count", ascending=False)
    )

    daily = (
        df.groupby("day_of_week", as_index=False)
        .agg(order_count=("order_count", "sum"), revenue=("revenue", "sum"))
        .sort_values("day_of_week")
    )

    monthly = (
        df.groupby("month", as_index=False)
        .agg(order_count=("order_count", "sum"), revenue=("revenue", "sum"))
        .sort_values("month")
    )

    print("\n=== Peak hours ===")
    print(tabulate(hourly.head(5), headers="keys", tablefmt="pretty", showindex=False))

    print("\n=== Weekday trend ===")
    print(tabulate(daily, headers="keys", tablefmt="pretty", showindex=False))

    print("\n=== Monthly trend ===")
    print(tabulate(monthly, headers="keys", tablefmt="pretty", showindex=False))


if __name__ == "__main__":
    main()
