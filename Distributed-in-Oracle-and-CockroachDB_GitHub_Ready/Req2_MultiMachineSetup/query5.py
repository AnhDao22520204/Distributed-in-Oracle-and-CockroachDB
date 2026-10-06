"""Query 5: Products with high ratings."""

from tabulate import tabulate

from distributed_query import query_all_partitions

QUERY = """
SELECT
    p.id AS product_id,
    p.name AS product_name,
    COUNT(r.id) AS review_count,
    AVG(r.rating) AS avg_rating,
    COUNT(DISTINCT r.user_id) AS unique_reviewers,
    COUNT(CASE WHEN r.rating >= 4 THEN 1 END) AS high_ratings,
    COUNT(CASE WHEN r.rating <= 2 THEN 1 END) AS low_ratings
FROM products p
JOIN reviews r ON r.product_id = p.id
JOIN stores s ON s.id = p.store_id
WHERE r.created_at >= CURRENT_DATE - INTERVAL '30 days'
  AND s.id BETWEEN %s AND %s
GROUP BY p.id, p.name
HAVING COUNT(r.id) >= 5
"""


def main():
    df = query_all_partitions(
        QUERY,
        [
            "product_id",
            "product_name",
            "review_count",
            "avg_rating",
            "unique_reviewers",
            "high_ratings",
            "low_ratings",
        ],
    )
    if df.empty:
        print("No data.")
        return

    for col in [
        "review_count",
        "avg_rating",
        "unique_reviewers",
        "high_ratings",
        "low_ratings",
    ]:
        df[col] = df[col].astype(float)

    result = (
        df.groupby(["product_id", "product_name"], as_index=False)
        .agg(
            review_count=("review_count", "sum"),
            avg_rating=("avg_rating", "mean"),
            unique_reviewers=("unique_reviewers", "sum"),
            high_ratings=("high_ratings", "sum"),
            low_ratings=("low_ratings", "sum"),
        )
    )

    result["high_rating_percent"] = (
        100 * result["high_ratings"] / result["review_count"]
    )
    result["low_rating_percent"] = (
        100 * result["low_ratings"] / result["review_count"]
    )
    result = result.sort_values(
        ["avg_rating", "review_count"],
        ascending=[False, False],
    ).head(15)

    print(tabulate(result, headers="keys", tablefmt="pretty", showindex=False))


if __name__ == "__main__":
    main()
