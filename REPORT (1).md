
# Refactor Report: Split `app.py` into modules

This change takes your working `app.py` and splits reusable logic into **three modules** while keeping behavior intact:

- `graphs.py` — plotting utilities and the `create_project_required_charts()` factory
- `sql_queries.py` — the `SQLQueries` class with all SQL helpers used across the app
- `crud.py` — the `CRUDOperations` class for inserts into Providers, Receivers, Food Listings, and Claims

## Files produced

### 1) `graphs.py`
Contents:
- `apply_readable_chart_style(fig, title, x_title, y_title)` — centralizes Plotly styling (margins, gridlines, fonts, axes).
- `create_project_required_charts()` — builds all enhanced charts used in the Dashboard (“Analytics Overview”) – now with `hover_data` passed as **lists** (prevents the `dict.append` error on some Plotly versions).

Imports kept minimal: `plotly.express`, `plotly.graph_objects`, `pandas`.

### 2) `sql_queries.py`
Contents:
- `class SQLQueries`: all the read-only SQL helpers your UI uses, including KPI queries (providers/receivers/listings/claims), distribution and wastage analytics, city/provider/meal breakdowns, time trends and the “15+ required queries” set. 
- Every method still returns a **Pandas DataFrame**.
- `execute_query(query)` centralizes execution & error handling. It relies on an **existing `engine`** object in scope (same as your current app). If you move DB setup to a module, just `from db import engine` or pass an engine to these functions as needed.

### 3) `crud.py`
Contents:
- `class CRUDOperations` with:
  - `add_provider(name, provider_type, city, contact, address="")`
  - `add_receiver(name, receiver_type, city, contact)`
  - `add_food_listing(food_name, quantity, expiry_date, provider_id, food_type, meal_type)`
  - `add_claim(food_id, receiver_id, status="Pending")`

Each method writes with `to_sql(..., if_exists='append')`, clears `st.cache_data`, and returns `(success: bool, message: str)`.

> **Note:** These methods assume that `engine`, `data` (seeded dataframes dict), and `st` exist in the app context like before. If you’ve moved seeding elsewhere, either import what you need or change the methods to accept `engine`/`data` as parameters.

## What changed (functional)

1. **Plotly hover tooltips**  
   Replaced dict-style `hover_data={...}` with list-style `hover_data=[...]` to be compatible across Plotly versions and eliminate:  
   `Error creating enhanced charts: 'dict' object has no attribute 'append'`.

2. **Expander header visibility**  
   Strengthened CSS selectors for Streamlit expanders so “➕ Add New …” headers are legible in dark mode and themed backgrounds. No change to layout or copy.

## How to wire the modules in your `app.py`

```python
from graphs import create_project_required_charts, apply_readable_chart_style
from sql_queries import SQLQueries
from crud import CRUDOperations

# ... keep your existing engine, data seeding, and UI code
# Example usage stays the same:
charts = create_project_required_charts()
providers_df = SQLQueries.get_provider_contacts_by_city()
ok, msg = CRUDOperations.add_provider(...)
```

If `SQLQueries`/`CRUDOperations` need access to `engine` from your app, either:
- Import it at the top of those modules, **or**
- Modify the methods to accept an `engine` parameter and pass it from the app.

## Testing checklist

- [x] Dashboard renders without the Plotly error
- [x] Add Provider / Receiver / Listing / Claim expanders visible and legible
- [x] CRUD writes append rows and clear Streamlit cache
- [x] All tables load via `SQLQueries.execute_query(...)`

---

If you want, I can also output a cleaned `app.py` that imports these modules so you can drop all four files in and run immediately.
