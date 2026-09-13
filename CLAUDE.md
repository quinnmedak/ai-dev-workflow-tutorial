# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a teaching repository (`ai-dev-workflow-tutorial`): a student works through `pre-work-setup.md` and `workshop-build-deploy.md` to build a Streamlit sales dashboard for a fictional PRD (`prd/ecommerce-analytics.md`), using Claude Code's Superpowers skills (brainstorming → writing-plans → executing-plans) end to end. The dashboard code itself is intentionally small; the point of the repo is the workflow, not the app.

## Commands

```bash
source venv/bin/activate               # activate the venv (plain venv + requirements.txt — no uv, no conda)
pip install -r requirements.txt

streamlit run app.py                   # run the dashboard locally (localhost:8501)

pytest tests/test_sales_data.py -v     # run the test suite
pytest tests/test_sales_data.py::test_name -v   # run a single test
```

`pytest.ini` sets `pythonpath = .` so bare `pytest` (not just `python -m pytest`) can find `sales_data.py` at the project root.

## Architecture

Two files, strict separation of concerns:

- **`sales_data.py`** — all data loading and calculation logic, pure functions over a `pd.DataFrame`, fully covered by `tests/test_sales_data.py`. `load_sales_data(csv_path)` reads `data/sales-data.csv` and validates required columns (`date, order_id, product, category, region, quantity, unit_price, total_amount`), raising `FileNotFoundError`/`ValueError`. The rest (`total_sales`, `total_orders`, `monthly_sales`, `sales_by_category`, `sales_by_region`) are one-shot aggregation functions consumed directly by `app.py`.
- **`app.py`** — Streamlit UI only, no calculation logic. Loads data via `sales_data.py` (cached with `@st.cache_data`), catches load errors with `st.error` + `st.stop()`, and renders KPI cards (`st.metric`), a monthly trend line, and category/region bar charts (Plotly Express).

This split is a deliberate constraint from the implementation plan, not incidental — new calculations belong in `sales_data.py` with tests, never inlined into `app.py`.

## Task tracking and traceability

`TASKS.md` is the project board (To Do / In Progress / Done), driven by `prd/ecommerce-analytics.md` and implemented via the plan at `docs/superpowers/plans/2026-09-13-sales-dashboard.md` (design doc: `docs/superpowers/specs/2026-09-13-sales-dashboard-design.md`). The plan's own "Plan Task" numbering does not map 1:1 to `TASKS.md` milestone IDs — see the plan's Milestone Map table (each `TASKS.md` TASK-N milestone typically spans a calculation-plus-tests plan task and a separate UI-wiring plan task).

Every commit that fulfills a milestone includes that milestone's ID in the message (e.g. `TASK-3: Add total_sales and total_orders calculations`), so `git log -- TASKS.md` shows the full history of milestones moving through the board. When a milestone is completed: push the code commits, then update `TASKS.md` (check off acceptance criteria, record the last code commit's hash on the `Commit:` line, add a `Notes:` line — "clean" if there were no deviations from the plan, otherwise what changed and why), move it to Done, commit that board update separately (e.g. `TASK-3: mark done on the board`), and push again.

Definition of done for any milestone: acceptance criteria met, `streamlit run app.py` runs cleanly, and commits carry the milestone ID.

## Lessons

Drawn from the `Notes:` lines recorded in `TASKS.md` as milestones were completed:

- Before committing, check exactly what's staged. Don't bundle a `TASKS.md` board edit (e.g. "move to In Progress") into the same commit as code changes — leftover staged files from a prior step will sneak in otherwise, and the two need separate commit messages anyway (TASK-1).
- Don't assume plan code snippets are current against the installed library versions — Streamlit (and libraries generally) deprecate APIs over time (e.g. `use_container_width` → `width`). Verify the app actually runs warning-free (a real browser session or `streamlit.testing.v1.AppTest`, not just a bare HTTP check) rather than trusting the plan's snippet as-is (TASK-6).
- Chart orientation/styling choices in a plan are a starting point, not final — the user may prefer horizontal bar charts over vertical ones (or other presentation tweaks) after seeing the dashboard rendered, even when the implementation already matches the plan exactly (TASK-5).
- Plain `pytest` only finds root-level modules like `sales_data.py` if `pythonpath = .` is set in `pytest.ini` — `python -m pytest` masks this because it adds the cwd to `sys.path` on its own (TASK-2).
