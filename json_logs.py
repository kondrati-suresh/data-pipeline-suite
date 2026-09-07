"""
json_logs.py
------------
Loads the website activity logs (JSON) and aggregates them per
employee so they can be joined onto the sales data - e.g. how many
quotes an employee generated online before the sale was recorded.
"""

import json
import pandas as pd
from config import WEBSITE_LOGS_JSON


def load_logs(path: str = WEBSITE_LOGS_JSON) -> pd.DataFrame:
    with open(path, "r") as f:
        raw_logs = json.load(f)
    return pd.DataFrame(raw_logs)


def aggregate_logs_by_employee(logs: pd.DataFrame) -> pd.DataFrame:
    """One row per employee_id with counts of each event type."""
    if logs.empty:
        return pd.DataFrame(columns=["employee_id", "quote_generated_count", "invoice_downloaded_count"])

    pivot = (
        logs.groupby(["employee_id", "event"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    pivot = pivot.rename(columns={
        "quote_generated": "quote_generated_count",
        "invoice_downloaded": "invoice_downloaded_count",
    })
    for col in ["quote_generated_count", "invoice_downloaded_count"]:
        if col not in pivot.columns:
            pivot[col] = 0
    return pivot[["employee_id", "quote_generated_count", "invoice_downloaded_count"]]


if __name__ == "__main__":
    logs = load_logs()
    summary = aggregate_logs_by_employee(logs)
    print(summary)
