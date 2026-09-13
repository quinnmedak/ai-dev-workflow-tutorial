# Design: E-Commerce Sales Dashboard

Source PRD: [prd/ecommerce-analytics.md](../../../prd/ecommerce-analytics.md)
Task board: [TASKS.md](../../../TASKS.md)

## Summary

A single-page Streamlit dashboard reading `data/sales-data.csv` (482 rows,
already in the repo) and displaying: two KPI cards (Total Sales, Total
Orders), a monthly sales trend line chart, and two bar charts (sales by
category, sales by region). No filters or date-range controls — Phase 1 is
explicitly a static, no-interactivity-beyond-tooltips view per the PRD's
scope boundary.

## Decisions

- **Trend granularity:** Monthly (12 points), not daily. Smoother and more
  readable for an executive audience; daily would be noisy at this volume.
- **Filters:** None. The PRD explicitly excludes "filtering and date range
  selection" from Phase 1 scope — the dashboard shows all 482 records.
- **CSV validation:** Basic guard only — check the file exists and required
  columns are present, raise a clear error otherwise. No per-row validation
  (type/null/range checks) — that's more robustness than a Phase 1 static
  dashboard needs.
- **Module structure:** Two files — `sales_data.py` (data loading +
  calculations) and `app.py` (Streamlit layout/UI). No separate `charts.py`
  or class-based wrapper; the app is small enough that a third split or an
  abstraction layer would add indirection without benefit.
- **Calculation function shape:** One small pure function per metric
  (`total_sales`, `total_orders`, `monthly_sales`, `sales_by_category`,
  `sales_by_region`) rather than one function returning everything, or a
  stateful class. Each function is independently unit-testable and maps
  1:1 to a PRD functional requirement (FR-1 through FR-4).

## Architecture & File Layout

```
ai-dev-workflow-tutorial/
├── app.py                  # Streamlit UI: layout, KPI cards, charts
├── sales_data.py           # Data loading + calculations (pytest-tested)
├── requirements.txt        # streamlit, pandas, plotly, pytest
├── venv/                   # plain Python venv (gitignored)
├── tests/
│   └── test_sales_data.py  # pytest tests for sales_data.py
└── data/
    └── sales-data.csv      # already exists
```

Dependencies are managed with a plain `venv/` + `requirements.txt` (no uv,
no conda), per project convention.

## Data Module Interface (`sales_data.py`)

```python
def load_sales_data(csv_path: str) -> pd.DataFrame:
    """Load and basic-validate the sales CSV (file exists, required columns present)."""

def total_sales(df: pd.DataFrame) -> float:
def total_orders(df: pd.DataFrame) -> int:
def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:      # columns: month, sales — sorted chronologically
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:  # columns: category, sales — sorted desc
def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:    # columns: region, sales — sorted desc
```

All functions except `load_sales_data` are pure functions of an
already-loaded DataFrame, so tests can use small in-memory fixture
DataFrames instead of touching the real CSV.

## App Layout (`app.py`)

`app.py` contains no calculation logic. It:

1. Calls `load_sales_data()` once, wrapped in `@st.cache_data` (supports the
   5-second load NFR-1).
2. Calls each `sales_data.py` function to get the numbers/chart data.
3. Renders, per the PRD's mockup:
   - Title bar
   - KPI row: Total Sales, Total Orders (`st.columns` + `st.metric`,
     currency/number formatted)
   - Monthly sales trend (Plotly line chart, `st.plotly_chart`, hover
     tooltips)
   - Two side-by-side bar charts: sales by category, sales by region (both
     sorted descending, hover tooltips)

## Error Handling

- `load_sales_data()` raises `FileNotFoundError` or `ValueError` with a
  plain-language message if the CSV is missing or required columns are
  absent.
- `app.py` catches that at startup and renders `st.error(...)` instead of
  letting a traceback surface, satisfying the PRD's "no errors" acceptance
  criterion.
- No per-row data validation — malformed individual rows flow through
  as-is (out of scope per the "basic guard" decision above).

## Testing Strategy

- `tests/test_sales_data.py`:
  - Unit tests per function using small in-memory fixture DataFrames
    (e.g., 3 known rows → assert the correct total).
  - One end-to-end sanity test that loads the real
    `data/sales-data.csv` and checks row count (482) and total sales
    (~$116,500) against the PRD's "Expected Output" table.
- `app.py` is not unit tested (Streamlit UI code isn't practical to unit
  test). It's verified manually by running `streamlit run app.py` and
  checking the result against the PRD's acceptance criteria — this is
  captured in TASKS.md's Definition of Done.

## Out of Scope (Phase 2, per PRD)

User authentication, real-time database integration, export functionality,
email alerts, filtering/date-range selection, drill-down, mobile-responsive
design. None of these are touched by this design.

## Milestone Mapping

This design covers all of TASKS.md's Phase 1 milestones (TASK-1 through
TASK-7): environment/project setup, data loading, KPI cards, trend chart,
category/region breakdowns, testing/refinement, and deployment. The
implementation plan (next step) will sequence concrete steps against each
milestone.
