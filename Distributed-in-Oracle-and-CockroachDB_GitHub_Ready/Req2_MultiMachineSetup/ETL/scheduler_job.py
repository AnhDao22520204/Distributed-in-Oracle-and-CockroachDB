import time
from datetime import date, timedelta

import schedule

from data_pipeline import (
    analyze_revenue_by_store,
    compute_stats,
    read_data_for_date,
    write_daily_report,
)


def job_daily_report():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    print(f"=== Daily report {yesterday} ===")

    data = read_data_for_date(yesterday)
    if data.empty:
        print("No invoices.")
        return

    summary = analyze_revenue_by_store(data)
    stats = compute_stats(data)
    write_daily_report(yesterday, summary)

    print(summary)
    print(stats)


if __name__ == "__main__":
    schedule.every().day.at("01:00").do(job_daily_report)
    print("Scheduler started. Job time: 01:00.")

    while True:
        schedule.run_pending()
        time.sleep(30)
