"""
schema_validator.py
--------------------
Solves part (b) of the assignment: "An API changes its response
structure without warning. Analyze how this could affect a Data
Science pipeline and propose mechanisms for detecting and handling
such changes."

Approach implemented here:
1. Define the EXPECTED_SCHEMA the pipeline was built against.
2. Before using a response, validate it against that schema.
3. If required top-level keys or per-record fields are missing (or new
   unexpected fields appear), raise a SchemaDriftError with a clear
   description of exactly what changed, instead of silently crashing
   deep inside the pipeline or - worse - silently producing wrong
   numbers (e.g. treating a missing field as 0).
"""

from dataclasses import dataclass, field


EXPECTED_SCHEMA = {
    "top_level_keys": {"location", "daily"},
    "daily_record_keys": {"date", "temp_max_c", "temp_min_c", "condition"},
}


@dataclass
class SchemaDriftReport:
    is_drifted: bool
    missing_top_level: set = field(default_factory=set)
    missing_daily_keys: set = field(default_factory=set)
    unexpected_daily_keys: set = field(default_factory=set)

    def describe(self) -> str:
        if not self.is_drifted:
            return "No schema drift detected."
        parts = []
        if self.missing_top_level:
            parts.append(f"missing top-level keys: {sorted(self.missing_top_level)}")
        if self.missing_daily_keys:
            parts.append(f"missing keys inside 'daily' records: {sorted(self.missing_daily_keys)}")
        if self.unexpected_daily_keys:
            parts.append(f"unexpected new keys inside 'daily' records: {sorted(self.unexpected_daily_keys)}")
        return "Schema drift detected -> " + "; ".join(parts)


class SchemaDriftError(Exception):
    pass


def check_schema(payload: dict) -> SchemaDriftReport:
    top_keys = set(payload.keys())
    missing_top = EXPECTED_SCHEMA["top_level_keys"] - top_keys

    missing_daily, unexpected_daily = set(), set()
    daily_records = payload.get("daily")
    if isinstance(daily_records, list) and daily_records:
        first_record_keys = set(daily_records[0].keys())
        missing_daily = EXPECTED_SCHEMA["daily_record_keys"] - first_record_keys
        unexpected_daily = first_record_keys - EXPECTED_SCHEMA["daily_record_keys"]

    is_drifted = bool(missing_top or missing_daily)
    return SchemaDriftReport(
        is_drifted=is_drifted,
        missing_top_level=missing_top,
        missing_daily_keys=missing_daily,
        unexpected_daily_keys=unexpected_daily,
    )


def validate_or_raise(payload: dict) -> None:
    report = check_schema(payload)
    if report.is_drifted:
        raise SchemaDriftError(report.describe())


if __name__ == "__main__":
    import json
    from config import WEATHER_SAMPLE_JSON, WEATHER_DRIFTED_JSON

    with open(WEATHER_SAMPLE_JSON) as f:
        good = json.load(f)
    print("good payload:", check_schema(good).describe())

    with open(WEATHER_DRIFTED_JSON) as f:
        drifted = json.load(f)
    print("drifted payload:", check_schema(drifted).describe())
