# Unified Multi-Source Data Integration & API Schema-Drift Pipeline

**Author:** Kondrati Suresh· **Register No.:** 113025148045 · **Batch:** 15
**Course:** Foundations of Artificial Intelligence — Innovative Assignment 1 (Micro Level Project)

## What this project does

Combines four different data sources into one unified analytical dataset:

| Source | Format | Role |
|---|---|---|
| `data/sales_sample.csv` | CSV | Core transactional sales records (stands in for a 5-million-row file) |
| `data/employees.xlsx` | Excel | Employee master data + manually typed correction notes |
| `data/website_logs.json` | JSON | Website activity (quotes/invoices) per employee |
| `data/weather_sample.json` (or live API) | JSON | Daily weather, joined onto sales by date |

It also detects and handles **API schema drift**: if the weather API's response
structure changes unexpectedly, the pipeline notices, logs exactly what
changed, and falls back to the last known-good data instead of silently
producing wrong numbers.

## Project structure

```
data-pipeline-project/
  src/
    config.py            # paths + register-number-based random seed
    csv_loader.py         # chunked, memory-efficient CSV reading + validation
    excel_corrections.py  # Excel load + manual-correction merging
    json_logs.py          # website log aggregation
    weather_api.py         # live API or offline mock, both schema-validated
    schema_validator.py   # schema drift detection
    integrator.py         # joins everything, cleans, summarises
    main.py                # runs the full pipeline end-to-end
  tests/
    test_schema_validator.py
    test_integrator.py
  data/                    # sample input files (see table above)
  docs/
    report_template.md
    architecture.md
  requirements.txt
  .gitignore
  LICENSE
  README.md
```

## Setup (from a fresh clone)

```bash
git clone <this-repo-url>
cd data-pipeline-project
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Before running, open `src/config.py` and set `REGISTER_NUMBER` to your
actual register number (all randomness in this project is seeded from it).

## Running the pipeline

```bash
python src/main.py
```

This prints progress for each stage and writes the final unified dataset to
`output/unified_dataset.csv`, followed by a revenue summary grouped by city
and weather condition.

## Running the tests

```bash
pytest tests/ -v
```

## Switching between live API and offline mock weather data

`src/weather_api.py` has a `MODE` variable at the top:

- `MODE = "mock"` (default) — always works, no internet needed, reads
  `data/weather_sample.json`.
- `MODE = "api"` — calls the free, key-less Open-Meteo API; if the call
  fails (no internet, timeout, or unexpected response shape) it automatically
  falls back to the mock file, so the pipeline never crashes.

To see schema-drift detection in action, point `weather_api._load_mock`
at `data/weather_sample_drifted.json` (or run `python src/schema_validator.py`
directly) — the console will print exactly which fields changed.

## Notes on the 5-million-record scenario

`csv_loader.py` reads the CSV with `pandas.read_csv(..., chunksize=...)`
rather than loading it all at once, so memory use stays roughly constant no
matter how large the real file is. The sample file included here is small on
purpose (a handful of rows) so the project runs instantly during evaluation,
but the exact same code path would handle a 5-million-row file — see
`docs/report_template.md` for the complexity discussion.
