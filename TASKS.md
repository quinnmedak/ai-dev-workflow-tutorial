# Tasks

This file tracks all work for the ShopSmart e-commerce analytics dashboard, as defined in [prd/ecommerce-analytics.md](prd/ecommerce-analytics.md).

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

### TASK-6: Testing and refinement
Verify the dashboard meets all acceptance criteria and polish the presentation.
- [ ] Dashboard loads within 5 seconds with no errors or warnings
- [ ] All PRD acceptance criteria checked off and verified against expected output values
- [ ] Layout and labels are clear enough for an executive presentation

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard and confirm public access.
- [ ] App deployed to Streamlit Community Cloud
- [ ] Public shareable URL loads the dashboard correctly
- [ ] Deployed version matches local behavior (no missing data or errors)

Commit:

## In Progress

## Done

### TASK-5: Category and region breakdowns
Add bar charts for sales by category and by region.
- [x] Category bar chart shows all 5 categories, sorted highest to lowest
- [x] Region bar chart shows all 4 regions, sorted highest to lowest
- [x] Both charts have interactive tooltips with exact values

Commit: 3c123c4
Notes: Changed category/region charts from vertical to horizontal bar charts per user request, after initial implementation matched the plan's vertical bars exactly.

### TASK-4: Sales trend chart
Add an interactive line chart showing sales over time.
- [x] Line chart renders sales by date/month with correct values
- [x] X-axis is time, Y-axis is sales amount
- [x] Tooltips show exact values on hover

Commit: 349970a
Notes: clean. No deviations from the plan.

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders as formatted KPI cards.
- [x] Total Sales displayed as currency (e.g., $116,500)
- [x] Total Orders displayed as a formatted count (482)
- [x] Values match expected calculations from the CSV

Commit: e37734c
Notes: clean. No deviations from the plan.

### TASK-2: Data loading and basic structure
Load sales-data.csv into a Pandas DataFrame and validate its structure.
- [x] CSV loads into a DataFrame with correct column types (date, numeric, categorical)
- [x] Basic validation confirms 482 records load without errors

Commit: 5dd88aa
Notes: Bare `pytest` couldn't find sales_data.py at the project root (only `python -m pytest` adds cwd to sys.path) — added pytest.ini with `pythonpath = .` so plain `pytest` works as documented in the plan. No other deviations.

### TASK-1: Environment setup and project initialization
Set up the Python project structure, dependencies, and Streamlit entry point.
- [x] Project structure created (app.py, data/, requirements.txt)
- [x] Dependencies (streamlit, pandas, plotly) install cleanly
- [x] `streamlit run app.py` launches a blank/placeholder app with no errors

Commit: b073f70
Notes: First pass, Claude accidentally bundled the TASKS.md "move to In Progress" edit into the same commit as app.py/requirements.txt (leftover staged files); had to reset and split them. That run was undone entirely and redone step-by-step in manual mode. No other deviations from the plan.
