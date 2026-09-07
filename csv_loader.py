"""
csv_loader.py
-------------
Reads the sales CSV in small chunks instead of loading the whole file
into memory at once.

Why this matters: the real assignment scenario is a 5,000,000-row CSV.
pandas.read_csv(path) with no chunksize loads the entire file into RAM
as one DataFrame, which can easily exceed available memory and crash
the process. Reading in chunks (CSV_CHUNK_SIZE rows at a time),
processing each chunk, and only keeping the columns/rows we actually
need keeps memory usage roughly constant regardless of file size.
"""

import pandas as pd
from config import SALES_CSV, CSV_CHUNK_SIZE

REQUIRED_COLUMNS = {
    "sale_id", "employee_id", "product", "quantity",
    "unit_price", "sale_date", "city",
}


def validate_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Basic data validation/cleaning applied to every chunk."""
    missing_cols = REQUIRED_COLUMNS - set(chunk.columns)
    if missing_cols:
        raise ValueError(f"sales CSV is missing required columns: {missing_cols}")

    # Drop rows with no employee_id or product - they cannot be joined later
    chunk = chunk.dropna(subset=["employee_id", "product"])

    # Coerce numeric columns; bad values become NaN and are dropped
    chunk["quantity"] = pd.to_numeric(chunk["quantity"], errors="coerce")
    chunk["unit_price"] = pd.to_numeric(chunk["unit_price"], errors="coerce")
    chunk = chunk.dropna(subset=["quantity", "unit_price"])

    chunk["sale_date"] = pd.to_datetime(chunk["sale_date"], errors="coerce")
    chunk = chunk.dropna(subset=["sale_date"])

    chunk["total_amount"] = chunk["quantity"] * chunk["unit_price"]
    return chunk


def load_sales_data(path: str = SALES_CSV, chunk_size: int = CSV_CHUNK_SIZE) -> pd.DataFrame:
    """Read the sales CSV chunk-by-chunk, validate each chunk, and
    concatenate the cleaned chunks into a single DataFrame.

    For a real 5-million-row file, replace the final concat with an
    incremental aggregation (e.g. writing each cleaned chunk straight
    to a database or a parquet file) so the whole cleaned dataset never
    has to sit in memory at once either.
    """
    cleaned_chunks = []
    total_rows_read = 0
    total_rows_kept = 0

    for chunk in pd.read_csv(path, chunksize=chunk_size):
        total_rows_read += len(chunk)
        cleaned = validate_chunk(chunk)
        total_rows_kept += len(cleaned)
        cleaned_chunks.append(cleaned)

    print(f"[csv_loader] read {total_rows_read} rows in chunks of {chunk_size}, "
          f"kept {total_rows_kept} valid rows")

    return pd.concat(cleaned_chunks, ignore_index=True)


if __name__ == "__main__":
    df = load_sales_data()
    print(df.head())
