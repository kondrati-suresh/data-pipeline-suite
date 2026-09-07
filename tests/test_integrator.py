import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from csv_loader import load_sales_data  # noqa: E402
from excel_corrections import load_employees, apply_corrections  # noqa: E402
from json_logs import load_logs, aggregate_logs_by_employee  # noqa: E402
from weather_api import fetch_weather  # noqa: E402
from integrator import build_unified_dataset  # noqa: E402


def test_sales_data_loads_and_has_total_amount():
    sales = load_sales_data()
    assert len(sales) > 0
    assert "total_amount" in sales.columns


def test_excel_correction_overrides_city():
    sales = load_sales_data()
    employees = load_employees()
    corrected = apply_corrections(sales, employees)

    # sale 1005 belongs to E002 and its note says the correct city is Chennai
    row = corrected[corrected["sale_id"] == 1005].iloc[0]
    assert row["city"] == "Chennai"


def test_unified_dataset_has_no_duplicate_sale_ids():
    sales = load_sales_data()
    employees = load_employees()
    corrected = apply_corrections(sales, employees)

    logs = load_logs()
    logs_summary = aggregate_logs_by_employee(logs)

    weather = fetch_weather()

    unified = build_unified_dataset(corrected, logs_summary, weather)
    assert unified["sale_id"].is_unique
    assert unified["temp_max_c"].isna().sum() == 0
