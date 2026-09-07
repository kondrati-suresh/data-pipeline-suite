"""
excel_corrections.py
---------------------
Loads the employees.xlsx file, which contains HR data plus manually
typed correction notes, and applies those corrections to the sales data.

In the real world, manual corrections in a spreadsheet are usually the
most trustworthy source (a human checked and fixed the value by hand),
so they should override whatever the automated CSV pipeline recorded.
"""

import re
import pandas as pd
from config import EMPLOYEES_XLSX


def load_employees(path: str = EMPLOYEES_XLSX) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="employees")
    df["manual_correction_note"] = df["manual_correction_note"].fillna("")
    return df


def parse_city_corrections(employees: pd.DataFrame) -> dict:
    """Extract {sale_id: corrected_city} pairs out of the free-text
    'manual_correction_note' column, e.g.:
    "sale 1005 city was mistyped as Hyderabad, correct city is Chennai"
    """
    corrections = {}
    pattern = re.compile(r"sale (\d+).*correct city is (\w+)", re.IGNORECASE)
    for note in employees["manual_correction_note"]:
        match = pattern.search(note)
        if match:
            sale_id, correct_city = match.groups()
            corrections[int(sale_id)] = correct_city
    return corrections


def apply_corrections(sales: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """Attach employee metadata (name/department) and apply manual
    city corrections on top of the raw CSV values."""
    sales = sales.merge(
        employees[["employee_id", "employee_name", "department", "home_city"]],
        on="employee_id",
        how="left",
    )

    corrections = parse_city_corrections(employees)
    for sale_id, correct_city in corrections.items():
        mask = sales["sale_id"] == sale_id
        sales.loc[mask, "city"] = correct_city

    return sales


if __name__ == "__main__":
    from csv_loader import load_sales_data

    sales = load_sales_data()
    employees = load_employees()
    corrected = apply_corrections(sales, employees)
    print(corrected[["sale_id", "employee_id", "city", "employee_name"]])
