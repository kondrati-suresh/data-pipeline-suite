"""
weather_api.py
---------------
Fetches daily weather data. Supports two modes so the project always
works during evaluation, even with no internet access:

    MODE = "api"    -> calls a real, free, no-key weather API
                       (Open-Meteo) for Chennai
    MODE = "mock"   -> reads data/weather_sample.json from disk

Every payload - whether from the real API or the mock file - is passed
through schema_validator before being used, so a schema change is
caught in one place regardless of where the data came from.
"""

import json
import urllib.request
import urllib.error

from config import WEATHER_SAMPLE_JSON
from schema_validator import validate_or_raise, SchemaDriftError

MODE = "mock"  # change to "api" to attempt a live call

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=13.08&longitude=80.27&daily=temperature_2m_max,temperature_2m_min"
    "&timezone=Asia%2FKolkata"
)


def _normalise_open_meteo(raw: dict) -> dict:
    """Open-Meteo's real response shape is different from the shape
    our pipeline expects, so we translate it into our internal
    {"location", "daily":[{...}]} shape here, in one place."""
    daily = raw.get("daily", {})
    dates = daily.get("time", [])
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])
    records = [
        {"date": d, "temp_max_c": h, "temp_min_c": l, "condition": "unknown"}
        for d, h, l in zip(dates, highs, lows)
    ]
    return {"location": "Chennai", "daily": records}


def fetch_weather() -> dict:
    if MODE == "api":
        try:
            with urllib.request.urlopen(OPEN_METEO_URL, timeout=5) as resp:
                raw = json.loads(resp.read())
            payload = _normalise_open_meteo(raw)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            print(f"[weather_api] live API call failed ({exc}); falling back to mock data")
            payload = _load_mock()
    else:
        payload = _load_mock()

    try:
        validate_or_raise(payload)
    except SchemaDriftError as exc:
        # Detected: log clearly and fall back to mock data rather than
        # letting bad/incomplete data flow silently into the pipeline.
        print(f"[weather_api] SCHEMA DRIFT DETECTED: {exc}")
        print("[weather_api] falling back to last known-good mock data")
        payload = _load_mock()

    return payload


def _load_mock() -> dict:
    with open(WEATHER_SAMPLE_JSON) as f:
        return json.load(f)


if __name__ == "__main__":
    data = fetch_weather()
    print(json.dumps(data, indent=2)[:500])
