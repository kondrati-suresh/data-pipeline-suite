"""
integrator.py
--------------
Joins the four cleaned sources into one unified analytical dataset:

    sales (CSV, corrected via Excel)  -- join on sale_date --> weather (API/mock)
    sales                              -- join on employee_id --> website logs summary

Also handles final missing-value filling and duplicate removal.
"""

import pandas as pd


def weather_to_dataframe(weather_payload: dict) -> pd.DataFrame:
    df = pd.DataFrame(weather_payload["daily"])
    df["date"] = pd.to_datetime(df["date"])
    return df


def build_unified_dataset(
    sales_with_corrections: pd.DataFrame,
    logs_summary: pd.DataFrame,
    weather_payload: dict,
) -> pd.DataFrame:
    df = sales_with_corrections.copy()

    # 1. Join website-log activity counts onto sales, by employee
    df = df.merge(logs_summary, on="employee_id", how="left")
    df["quote_generated_count"] = df["quote_generated_count"].fillna(0).astype(int)
    df["invoice_downloaded_count"] = df["invoice_downloaded_count"].fillna(0).astype(int)

    # 2. Join weather onto sales, by date
    weather_df = weather_to_dataframe(weather_payload)
    df = df.merge(
        weather_df,
        left_on="sale_date",
        right_on="date",
        how="left",
        suffixes=("", "_weather"),
    )
    df = df.drop(columns=["date"])

    # 3. Missing-value handling for anything weather couldn't cover
    #    (e.g. a sale date outside the weather sample's date range)
    df["condition"] = df["condition"].fillna("no_data")
    df["temp_max_c"] = df["temp_max_c"].fillna(df["temp_max_c"].mean())
    df["temp_min_c"] = df["temp_min_c"].fillna(df["temp_min_c"].mean())

    # 4. Duplicate handling - a sale_id should be unique
    before = len(df)
    df = df.drop_duplicates(subset=["sale_id"], keep="first")
    removed = before - len(df)
    if removed:
        print(f"[integrator] removed {removed} duplicate sale_id row(s)")

    return df


def summarise(df: pd.DataFrame) -> pd.DataFrame:
    """Basic analytical summary: revenue by city and by weather condition."""
    return (
        df.groupby(["city", "condition"])
        .agg(total_revenue=("total_amount", "sum"), num_sales=("sale_id", "count"))
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
