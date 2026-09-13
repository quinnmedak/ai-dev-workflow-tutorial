# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ShopSmart Streamlit sales dashboard (KPIs, trend chart, category/region breakdowns) reading `data/sales-data.csv`, per the approved design.

**Architecture:** Two files — `sales_data.py` (pure, pytest-tested data loading/calculation functions) and `app.py` (Streamlit UI only, no calculation logic). See interfaces below.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly, pytest. Plain `venv/` + `requirements.txt` — no uv, no conda.

**Spec:** [docs/superpowers/specs/2026-09-13-sales-dashboard-design.md](../specs/2026-09-13-sales-dashboard-design.md)

## Global Constraints

- Work on the current git branch `feature/sales-dashboard`. Do not create a worktree or a new branch.
- Dependencies via a plain `venv/` virtual environment + `requirements.txt` only (no uv, no conda).
- All calculation logic lives in `sales_data.py`, tested with pytest in `tests/test_sales_data.py`. `app.py` contains no calculation logic — UI/layout only.
- Keep code simple and readable — no abstractions beyond what's specified (no classes, no `charts.py` split — see design doc).
- Every commit message includes the TASKS.md milestone ID it belongs to (e.g. `TASK-3: ...`), per TASKS.md's Definition of Done.
- CSV validation is a basic guard only: check file exists and required columns are present. No per-row validation.
- Trend chart is monthly granularity. No filters or date-range controls anywhere in the UI.

---

## Milestone Map

| Plan Task | TASKS.md Milestone |
|---|---|
| Plan Task 1 | TASK-1: Environment setup and project initialization |
| Plan Task 2 | TASK-2: Data loading and basic structure |
| Plan Task 3, 4 | TASK-3: KPI cards implementation |
| Plan Task 5, 6 | TASK-4: Sales trend chart |
| Plan Task 7, 8 | TASK-5: Category and region breakdowns |
| Plan Task 9 | TASK-6: Testing and refinement |
| Plan Task 10 | TASK-7: Deployment (**user-executed**, not part of this plan's automated work) |

---

### Plan Task 1: Environment setup and project scaffolding

**Milestone: TASK-1**

**Files:**
- Create: `requirements.txt`
- Create: `app.py` (placeholder)
- Create: `venv/` (not committed — already gitignored)

**Interfaces:**
- Produces: a working `venv/` with `streamlit`, `pandas`, `plotly`, `pytest` installed, and a placeholder `app.py` that later tasks will build on.

- [ ] **Step 1: Create the virtual environment**

Run: `python3 -m venv venv`
Expected: a `venv/` directory is created (already covered by `.gitignore`).

- [ ] **Step 2: Write `requirements.txt`**

```
streamlit>=1.38
pandas>=2.2
plotly>=5.24
pytest>=8.3
```

- [ ] **Step 3: Activate the venv and install dependencies**

Run:
```bash
source venv/bin/activate
pip install -r requirements.txt
```
Expected: all four packages install with no errors.

- [ ] **Step 4: Write a placeholder `app.py`**

```python
import streamlit as st

st.title("ShopSmart Sales Dashboard")
st.write("Dashboard under construction.")
```

- [ ] **Step 5: Verify the app launches**

Run: `streamlit run app.py`
Expected: browser opens to `localhost:8501` showing the title and placeholder text, no errors in the terminal. Stop the server (Ctrl+C) once confirmed.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app.py
git commit -m "TASK-1: Set up venv, requirements.txt, and placeholder app"
```

---

### Plan Task 2: Data loading with validation

**Milestone: TASK-2**

**Files:**
- Create: `sales_data.py`
- Create: `tests/test_sales_data.py`

**Interfaces:**
- Produces: `load_sales_data(csv_path: str) -> pd.DataFrame`, raising `FileNotFoundError` if the path doesn't exist and `ValueError` if required columns are missing. Required columns: `date, order_id, product, category, region, quantity, unit_price, total_amount`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_sales_data.py
import pandas as pd
import pytest
from sales_data import load_sales_data

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def test_load_sales_data_returns_dataframe_with_required_columns():
    df = load_sales_data("data/sales-data.csv")
    assert isinstance(df, pd.DataFrame)
    for column in REQUIRED_COLUMNS:
        assert column in df.columns


def test_load_sales_data_reads_all_rows():
    df = load_sales_data("data/sales-data.csv")
    assert len(df) == 482


def test_load_sales_data_missing_file_raises_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        load_sales_data("data/does-not-exist.csv")


def test_load_sales_data_missing_required_column_raises_value_error(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("date,order_id,product\n2024-01-01,ORD-1,Widget\n")
    with pytest.raises(ValueError):
        load_sales_data(str(bad_csv))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_sales_data.py -v`
Expected: all four tests FAIL with `ModuleNotFoundError: No module named 'sales_data'` (module doesn't exist yet).

- [ ] **Step 3: Write the minimal implementation**

```python
# sales_data.py
import os
import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def load_sales_data(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Sales data file not found: {csv_path}")

    df = pd.read_csv(csv_path, parse_dates=["date"])

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Sales data is missing required columns: {missing}")

    return df
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_sales_data.py -v`
Expected: all four tests PASS.

- [ ] **Step 5: Commit**

```bash
git add sales_data.py tests/test_sales_data.py
git commit -m "TASK-2: Add load_sales_data with basic CSV validation"
```

---

### Plan Task 3: `total_sales` and `total_orders` calculations

**Milestone: TASK-3**

**Files:**
- Modify: `sales_data.py`
- Modify: `tests/test_sales_data.py`

**Interfaces:**
- Consumes: a `pd.DataFrame` as returned by `load_sales_data` (must have a `total_amount` column).
- Produces: `total_sales(df: pd.DataFrame) -> float`, `total_orders(df: pd.DataFrame) -> int`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_sales_data.py`:

```python
from sales_data import total_sales, total_orders


def _fixture_df():
    return pd.DataFrame({
        "total_amount": [100.0, 50.0, 25.0],
    })


def test_total_sales_sums_total_amount():
    assert total_sales(_fixture_df()) == 175.0


def test_total_orders_counts_rows():
    assert total_orders(_fixture_df()) == 3


def test_total_sales_matches_expected_value_for_real_data():
    df = load_sales_data("data/sales-data.csv")
    assert total_sales(df) == pytest.approx(116500.21, abs=0.01)


def test_total_orders_matches_expected_value_for_real_data():
    df = load_sales_data("data/sales-data.csv")
    assert total_orders(df) == 482
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_sales_data.py -v`
Expected: the four new tests FAIL with `ImportError: cannot import name 'total_sales'`.

- [ ] **Step 3: Write the minimal implementation**

Append to `sales_data.py`:

```python
def total_sales(df: pd.DataFrame) -> float:
    return float(df["total_amount"].sum())


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_sales_data.py -v`
Expected: all tests PASS (8 total so far).

- [ ] **Step 5: Commit**

```bash
git add sales_data.py tests/test_sales_data.py
git commit -m "TASK-3: Add total_sales and total_orders calculations"
```

---

### Plan Task 4: KPI cards in the UI

**Milestone: TASK-3**

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `sales_data.load_sales_data`, `sales_data.total_sales`, `sales_data.total_orders`.

- [ ] **Step 1: Replace the placeholder `app.py` with data loading and KPI cards**

```python
# app.py
import streamlit as st
from sales_data import load_sales_data, total_sales, total_orders

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_data():
    return load_sales_data("data/sales-data.csv")


st.title("ShopSmart Sales Dashboard")

try:
    df = get_data()
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.2f}")
col2.metric("Total Orders", f"{total_orders(df):,}")
```

- [ ] **Step 2: Verify manually**

Run: `streamlit run app.py`
Expected: page shows "Total Sales" as `$116,500.21` and "Total Orders" as `482`, no errors in terminal. Stop the server once confirmed.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-3: Display Total Sales and Total Orders KPI cards"
```

---

### Plan Task 5: `monthly_sales` calculation

**Milestone: TASK-4**

**Files:**
- Modify: `sales_data.py`
- Modify: `tests/test_sales_data.py`

**Interfaces:**
- Consumes: a `pd.DataFrame` with `date` (datetime64) and `total_amount` columns.
- Produces: `monthly_sales(df: pd.DataFrame) -> pd.DataFrame` with columns `month` (string, e.g. `"2024-01"`) and `sales` (float), sorted chronologically ascending.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_sales_data.py`:

```python
from sales_data import monthly_sales


def test_monthly_sales_groups_by_month_and_sums():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-10"]),
        "total_amount": [100.0, 50.0, 25.0],
    })
    result = monthly_sales(df)
    assert list(result["month"]) == ["2024-01", "2024-02"]
    assert list(result["sales"]) == [150.0, 25.0]


def test_monthly_sales_sorted_chronologically():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-03-01", "2024-01-01", "2024-02-01"]),
        "total_amount": [1.0, 1.0, 1.0],
    })
    result = monthly_sales(df)
    assert list(result["month"]) == ["2024-01", "2024-02", "2024-03"]


def test_monthly_sales_has_twelve_months_for_real_data():
    df = load_sales_data("data/sales-data.csv")
    result = monthly_sales(df)
    assert len(result) == 12
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_sales_data.py -v`
Expected: the three new tests FAIL with `ImportError: cannot import name 'monthly_sales'`.

- [ ] **Step 3: Write the minimal implementation**

Append to `sales_data.py`:

```python
def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    monthly = df.copy()
    monthly["month"] = monthly["date"].dt.strftime("%Y-%m")
    result = monthly.groupby("month")["total_amount"].sum().reset_index()
    result = result.rename(columns={"total_amount": "sales"})
    return result.sort_values("month").reset_index(drop=True)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_sales_data.py -v`
Expected: all tests PASS (11 total so far).

- [ ] **Step 5: Commit**

```bash
git add sales_data.py tests/test_sales_data.py
git commit -m "TASK-4: Add monthly_sales calculation"
```

---

### Plan Task 6: Sales trend line chart in the UI

**Milestone: TASK-4**

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `sales_data.monthly_sales`.

- [ ] **Step 1: Add the trend chart**

Add to `app.py`, after the KPI cards block, and add `import plotly.express as px` to the imports:

```python
import plotly.express as px
```

```python
st.subheader("Sales Trend Over Time")
monthly = monthly_sales(df)
trend_fig = px.line(monthly, x="month", y="sales", markers=True)
trend_fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
st.plotly_chart(trend_fig, use_container_width=True)
```

Also add `monthly_sales` to the `from sales_data import ...` line.

- [ ] **Step 2: Verify manually**

Run: `streamlit run app.py`
Expected: a line chart with 12 points (Jan–Dec 2024) appears below the KPI cards; hovering a point shows the exact month and sales value. No errors in terminal. Stop the server once confirmed.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-4: Add sales trend line chart"
```

---

### Plan Task 7: `sales_by_category` and `sales_by_region` calculations

**Milestone: TASK-5**

**Files:**
- Modify: `sales_data.py`
- Modify: `tests/test_sales_data.py`

**Interfaces:**
- Consumes: a `pd.DataFrame` with `category`/`region` and `total_amount` columns.
- Produces: `sales_by_category(df) -> pd.DataFrame` with columns `category`, `sales`, sorted by `sales` descending. `sales_by_region(df) -> pd.DataFrame` with columns `region`, `sales`, sorted by `sales` descending.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_sales_data.py`:

```python
from sales_data import sales_by_category, sales_by_region


def test_sales_by_category_groups_and_sorts_descending():
    df = pd.DataFrame({
        "category": ["Audio", "Electronics", "Audio"],
        "total_amount": [10.0, 100.0, 5.0],
    })
    result = sales_by_category(df)
    assert list(result["category"]) == ["Electronics", "Audio"]
    assert list(result["sales"]) == [100.0, 15.0]


def test_sales_by_region_groups_and_sorts_descending():
    df = pd.DataFrame({
        "region": ["South", "North", "South"],
        "total_amount": [10.0, 100.0, 5.0],
    })
    result = sales_by_region(df)
    assert list(result["region"]) == ["North", "South"]
    assert list(result["sales"]) == [100.0, 15.0]


def test_sales_by_category_matches_real_data_top_category():
    df = load_sales_data("data/sales-data.csv")
    result = sales_by_category(df)
    assert result.iloc[0]["category"] == "Electronics"
    assert len(result) == 5


def test_sales_by_region_matches_real_data_all_regions():
    df = load_sales_data("data/sales-data.csv")
    result = sales_by_region(df)
    assert set(result["region"]) == {"North", "South", "East", "West"}
    assert len(result) == 4
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_sales_data.py -v`
Expected: the four new tests FAIL with `ImportError: cannot import name 'sales_by_category'`.

- [ ] **Step 3: Write the minimal implementation**

Append to `sales_data.py`:

```python
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("category")["total_amount"].sum().reset_index()
    result = result.rename(columns={"total_amount": "sales"})
    return result.sort_values("sales", ascending=False).reset_index(drop=True)


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("region")["total_amount"].sum().reset_index()
    result = result.rename(columns={"total_amount": "sales"})
    return result.sort_values("sales", ascending=False).reset_index(drop=True)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_sales_data.py -v`
Expected: all tests PASS (15 total so far).

- [ ] **Step 5: Commit**

```bash
git add sales_data.py tests/test_sales_data.py
git commit -m "TASK-5: Add sales_by_category and sales_by_region calculations"
```

---

### Plan Task 8: Category and region bar charts in the UI

**Milestone: TASK-5**

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `sales_data.sales_by_category`, `sales_data.sales_by_region`.

- [ ] **Step 1: Add the two bar charts side by side**

Add to `app.py`, after the trend chart block. Add `sales_by_category, sales_by_region` to the `from sales_data import ...` line.

```python
st.subheader("Category and Region Breakdown")
col3, col4 = st.columns(2)

with col3:
    st.write("Sales by Category")
    category_df = sales_by_category(df)
    category_fig = px.bar(category_df, x="category", y="sales")
    category_fig.update_layout(xaxis_title="Category", yaxis_title="Sales ($)")
    st.plotly_chart(category_fig, use_container_width=True)

with col4:
    st.write("Sales by Region")
    region_df = sales_by_region(df)
    region_fig = px.bar(region_df, x="region", y="sales")
    region_fig.update_layout(xaxis_title="Region", yaxis_title="Sales ($)")
    st.plotly_chart(region_fig, use_container_width=True)
```

- [ ] **Step 2: Verify manually**

Run: `streamlit run app.py`
Expected: two bar charts side by side below the trend chart. Category chart shows 5 bars sorted descending with Electronics tallest. Region chart shows 4 bars sorted descending with North tallest. Hover tooltips show exact values. No errors in terminal. Stop the server once confirmed.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-5: Add category and region breakdown bar charts"
```

---

### Plan Task 9: Testing and refinement

**Milestone: TASK-6**

**Files:**
- Modify: `tests/test_sales_data.py`
- Modify: `app.py` (only if issues are found below)

**Interfaces:**
- None new — this task verifies existing behavior end-to-end.

- [ ] **Step 1: Add an end-to-end sanity test tying together all calculations against the PRD's expected output**

Append to `tests/test_sales_data.py`:

```python
def test_full_dataset_matches_prd_expected_output():
    df = load_sales_data("data/sales-data.csv")
    assert total_orders(df) == 482
    assert total_sales(df) == pytest.approx(116500.21, abs=0.01)
    assert sales_by_category(df).iloc[0]["category"] == "Electronics"
    assert set(sales_by_region(df)["region"]) == {"North", "South", "East", "West"}
```

- [ ] **Step 2: Run the full test suite**

Run: `pytest tests/test_sales_data.py -v`
Expected: all tests PASS (16 total).

- [ ] **Step 3: Manually verify the error path**

Run:
```bash
python3 -c "
import shutil
shutil.move('data/sales-data.csv', 'data/sales-data.csv.bak')
"
streamlit run app.py
```
Expected: the app shows `st.error("Could not load sales data: Sales data file not found: data/sales-data.csv")` instead of crashing. Stop the server, then restore the file:
```bash
python3 -c "
import shutil
shutil.move('data/sales-data.csv.bak', 'data/sales-data.csv')
"
```

- [ ] **Step 4: Full manual run-through against the PRD acceptance criteria**

Run: `streamlit run app.py` and confirm each PRD acceptance criterion (prd/ecommerce-analytics.md, "Acceptance Criteria" section):
- KPIs visible: Total Sales (~$116,500.21) and Total Orders (482) displayed prominently.
- Trend chart works: line chart shows monthly sales, matches CSV data.
- Category chart works: bar chart sorted descending, Electronics highest.
- Region chart works: bar chart sorted descending, North highest.
- Data loads correctly: no discrepancies vs. the values computed above.
- No errors: no exceptions or warnings in the browser or terminal.
- Professional appearance: consistent spacing/labels, suitable for a presentation.

Stop the server once confirmed. If any criterion fails, fix the specific issue in `app.py` or `sales_data.py`, re-run this step, and note the fix in the commit message.

- [ ] **Step 5: Commit**

```bash
git add tests/test_sales_data.py
git commit -m "TASK-6: Add end-to-end sanity test and verify PRD acceptance criteria"
```

---

### Plan Task 10: Deployment — performed by the user

**Milestone: TASK-7**

**This step is not executed as part of this plan.** Deployment is performed by the user (Quinn), manually, after this branch is merged to `main`. No agent/automated work happens here — this task exists only to record the handoff and close out TASKS.md.

**User steps (for reference, not for the agent to run):**
1. Merge `feature/sales-dashboard` into `main` (e.g. via PR, following the project's normal review process).
2. From `main`, deploy the app to Streamlit Community Cloud (https://share.streamlit.io), pointing at `app.py` with `requirements.txt` for dependencies.
3. Confirm the public URL loads the dashboard and matches local behavior (KPIs, trend chart, category/region charts all render correctly, no errors).
4. Update `TASKS.md`: move `TASK-7` to Done, filling in the `Commit:` line and noting the deployed URL.

---

## Self-Review Notes

- **Spec coverage:** Every design doc section is covered — file layout (Task 1), `load_sales_data` + validation (Task 2), all five calculation functions (Tasks 3, 5, 7), KPI cards / trend chart / category+region charts in `app.py` (Tasks 4, 6, 8), error handling verification (Task 9), testing strategy including the real-CSV sanity check (Tasks 2, 3, 5, 7, 9). Deployment (Task 10) is explicitly out of the agent's execution scope per the user's ground rules.
- **Placeholder scan:** No TBD/TODO markers; every step has concrete code or an exact command.
- **Type consistency:** Function names and return shapes (`month`/`sales` columns, `category`/`sales`, `region`/`sales`) are used identically across the calculation tasks and the UI tasks that consume them.
