# Data Flow (text diagram)

```
 sales_sample.csv                employees.xlsx
 (chunked read,      ---->       (manual correction
  validated)                      notes, parsed)
        \                              /
         \                            /
          v                          v
              apply_corrections()
                     |
                     v
          sales_corrected (DataFrame)
                     |
     +---------------+----------------+
     |                                |
     v                                v
website_logs.json                weather_sample.json
(aggregated per                  or live API
 employee_id)                    (schema-validated;
     |                            falls back to mock
     |                            on drift)
     v                                v
          build_unified_dataset()
                     |
                     v
        missing-value fill + de-dup
                     |
                     v
          output/unified_dataset.csv
                     |
                     v
            summarise() -> printed
            revenue-by-city report
```

Join keys:
- `sales.employee_id` <-> `employees.employee_id` (Excel corrections + names)
- `sales.employee_id` <-> `website_logs.employee_id` (activity counts)
- `sales.sale_date` <-> `weather.date` (daily conditions)
