"""
config.py
---------
Central place for paths and the random seed.

IMPORTANT (assignment requirement): all randomness in this project must be
seeded using the student's register number. Replace REGISTER_NUMBER below
with your actual register number before you commit your final version.
"""

import os

# TODO: replace this with your real register number, e.g. 22CS1234
REGISTER_NUMBER = "REPLACE_WITH_YOUR_REGISTER_NUMBER"

def get_seed() -> int:
    """Turn the register number into a deterministic integer seed.

    We sum the character codes of the register number so that any
    alphanumeric register number produces a stable, reproducible seed.
    """
    return sum(ord(ch) for ch in REGISTER_NUMBER)

SEED = get_seed()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

SALES_CSV = os.path.join(DATA_DIR, "sales_sample.csv")
EMPLOYEES_XLSX = os.path.join(DATA_DIR, "employees.xlsx")
WEBSITE_LOGS_JSON = os.path.join(DATA_DIR, "website_logs.json")
WEATHER_SAMPLE_JSON = os.path.join(DATA_DIR, "weather_sample.json")
WEATHER_DRIFTED_JSON = os.path.join(DATA_DIR, "weather_sample_drifted.json")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
UNIFIED_OUTPUT_CSV = os.path.join(OUTPUT_DIR, "unified_dataset.csv")

# Chunk size used when reading the (simulated) 5-million-record CSV.
# Real file would be read in chunks of this many rows at a time instead
# of loading everything into memory at once.
CSV_CHUNK_SIZE = 500
