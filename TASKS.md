# Tasks

This file tracks all work for the ShopSmart e-commerce analytics dashboard, as defined in [prd/ecommerce-analytics.md](prd/ecommerce-analytics.md).

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders as formatted KPI cards.
- [ ] Total Sales displayed as currency (e.g., $116,500)
- [ ] Total Orders displayed as a formatted count (482)
- [ ] Values match expected calculations from the CSV

Commit:

### TASK-4: Sales trend chart
Add an interactive line chart showing sales over time.
- [ ] Line chart renders sales by date/month with correct values
- [ ] X-axis is time, Y-axis is sales amount
- [ ] Tooltips show exact values on hover

Commit:

### TASK-5: Category and region breakdowns
Add bar charts for sales by category and by region.
- [ ] Category bar chart shows all 5 categories, sorted highest to lowest
- [ ] Region bar chart shows all 4 regions, sorted highest to lowest
- [ ] Both charts have interactive tooltips with exact values

Commit:

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

### TASK-2: Data loading and basic structure
Load sales-data.csv into a Pandas DataFrame and validate its structure.
- [ ] CSV loads into a DataFrame with correct column types (date, numeric, categorical)
- [ ] Basic validation confirms 482 records load without errors

Commit:

## Done

### TASK-1: Environment setup and project initialization
Set up the Python project structure, dependencies, and Streamlit entry point.
- [x] Project structure created (app.py, data/, requirements.txt)
- [x] Dependencies (streamlit, pandas, plotly) install cleanly
- [x] `streamlit run app.py` launches a blank/placeholder app with no errors

Commit: b073f70
Notes: First pass, Claude accidentally bundled the TASKS.md "move to In Progress" edit into the same commit as app.py/requirements.txt (leftover staged files); had to reset and split them. That run was undone entirely and redone step-by-step in manual mode. No other deviations from the plan.
