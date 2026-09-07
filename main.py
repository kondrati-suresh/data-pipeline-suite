"""
main.py
-------
Runs the full pipeline end to end:

    CSV (chunked) -> apply Excel corrections -> aggregate JSON logs
    -> fetch weather (API or mock, schema-validated) -> integrate
    -> clean -> write unified_dataset.csv -> print analytical summary

Run with:  python src/main.py
"""

import os
import random

import numpy as np

from config import SEED, OUTPUT_DIR, UNIFIED_OUTPUT_CSV, REGISTER_NUMBER
from csv_loader import load_sales_data
from excel_corrections import load_employees, apply_corrections
from json_logs import load_logs, aggregate_logs_by_employee
from weather_api import fetch_weather
from integrator import build_unified_dataset, summarise


def main():
    random.seed(SEED)
    np.random.seed(SEED)
    print(f"[main] register number: {REGISTER_NUMBER!r} -> random seed: {SEED}")

    print("\n[main] Step 1/4: loading + validating sales CSV (chunked read)")
    sales = load_sales_data()

    print("\n[main] Step 2/4: applying Excel manual corrections")
    employees = load_employees()
    sales_corrected = apply_corrections(sales, employees)

    print("\n[main] Step 3/4: aggregating website JSON logs")
    logs = load_logs()
    logs_summary = aggregate_logs_by_employee(logs)

    print("\n[main] Step 4/4: fetching + validating weather data")
    weather_payload = fetch_weather()

    print("\n[main] integrating all four sources into one dataset")
    unified = build_unified_dataset(sales_corrected, logs_summary, weather_payload)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    unified.to_csv(UNIFIED_OUTPUT_CSV, index=False)
    print(f"\n[main] wrote unified dataset -> {UNIFIED_OUTPUT_CSV}  ({len(unified)} rows)")

    print("\n[main] Analytical summary (revenue by city & weather condition):")
    print(summarise(unified).to_string(index=False))


if __name__ == "__main__":
    main()
