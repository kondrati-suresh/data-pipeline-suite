# Report: Unified Multi-Source Data Integration & API Schema-Drift Pipeline

**Name:** Kashifa Farheen S A **Register No.:** ______ **Batch:** 15

## 1. Problem Formulation
- State the two problems given in the assignment in your own words:
  (a) integrating CSV + Excel + API data, including a 5-million-row CSV,
      an Excel file of manual corrections, and daily API updates;
  (b) handling an API that silently changes its response structure.
- Explain why this matters in a real data pipeline (broken dashboards,
  wrong business decisions, pipeline crashes).

## 2. Approach
- Describe the four sources and the unified schema you produced.
- Explain chunked CSV reading and why it keeps memory usage constant.
- Explain how Excel corrections are matched to sale records and why
  manual corrections should override automated data.
- Explain the schema-validation approach: expected schema, drift
  detection, fallback strategy. Include the schema-drift test result
  (`weather_sample_drifted.json`) as your example.

## 3. Complexity
- CSV loader: O(n) time over n rows, O(chunk_size) memory instead of O(n).
- Merges: pandas merge is roughly O(n log n) (hash/sort join).
- Schema check: O(1) — only looks at the top-level keys and one record.
- Discuss how this scales to the real 5-million-row case.

## 4. Results
- Insert a screenshot of `python src/main.py` running successfully.
- Insert a screenshot of `pytest tests/ -v` passing.
- Include the printed revenue-by-city/condition summary table.
- Comparison: show the console output before vs. after the Excel
  correction is applied for sale_id 1005 or 1012 (city changes).
- Comparison: show console output for a clean weather payload vs. the
  drifted payload, highlighting the drift message that gets printed.

## 5. Reflection
- What was hardest to get right (e.g. matching correction notes,
  designing the fallback logic)?
- What would you change for a true 5-million-row production pipeline
  (e.g. write to a database instead of concatenating chunks in memory,
  add retries/alerting for the API)?
- What did you learn about robustness in data pipelines?
