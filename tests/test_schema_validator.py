import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schema_validator import check_schema  # noqa: E402


def test_good_schema_not_drifted():
    payload = {
        "location": "Chennai",
        "daily": [{"date": "2024-01-05", "temp_max_c": 29.0, "temp_min_c": 22.0, "condition": "Sunny"}],
    }
    report = check_schema(payload)
    assert report.is_drifted is False


def test_missing_top_level_key_detected():
    payload = {"daily": [{"date": "2024-01-05", "temp_max_c": 29.0, "temp_min_c": 22.0, "condition": "Sunny"}]}
    report = check_schema(payload)
    assert report.is_drifted is True
    assert "location" in report.missing_top_level


def test_renamed_daily_fields_detected():
    payload = {
        "location": "Chennai",
        "daily": [{"date": "2024-01-05", "max_temp": 29.0, "min_temp": 22.0, "sky": "Sunny"}],
    }
    report = check_schema(payload)
    assert report.is_drifted is True
    assert {"temp_max_c", "temp_min_c", "condition"} <= report.missing_daily_keys
    assert {"max_temp", "min_temp", "sky"} <= report.unexpected_daily_keys


def test_real_drifted_sample_file():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "weather_sample_drifted.json")
    with open(path) as f:
        payload = json.load(f)
    report = check_schema(payload)
    assert report.is_drifted is True
