import streamlit as st
import plotly.express as px
from sales_data import (
    load_sales_data,
    total_sales,
    total_orders,
    monthly_sales,
    sales_by_category,
    sales_by_region,
)

# Fixed, muted categorical palette, assigned by entity name (not by sort
# rank) so colors stay stable if the underlying data changes.
CATEGORY_COLORS = {
    "Electronics": "#5b7c99",
    "Accessories": "#b3714f",
    "Audio": "#7a9471",
    "Wearables": "#b39659",
    "Smart Home": "#9b7d95",
}
REGION_COLORS = {
    "North": "#5b7c99",
    "South": "#b3714f",
    "East": "#7a9471",
    "West": "#b39659",
}
TREND_COLOR = "#5b7c99"

CHART_CHROME = {
    "gridcolor": "#e1e0d9",
    "linecolor": "#c3c2b7",
    "tickfont_color": "#898781",
}


def style_axes(fig):
    fig.update_layout(plot_bgcolor="white", margin=dict(t=20, b=10))
    fig.update_xaxes(
        gridcolor=CHART_CHROME["gridcolor"],
        linecolor=CHART_CHROME["linecolor"],
        tickfont_color=CHART_CHROME["tickfont_color"],
    )
    fig.update_yaxes(
        gridcolor=CHART_CHROME["gridcolor"],
        linecolor=CHART_CHROME["linecolor"],
        tickfont_color=CHART_CHROME["tickfont_color"],
    )
    return fig


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

st.divider()

st.subheader("Sales Trend Over Time")
monthly = monthly_sales(df)
trend_fig = px.line(monthly, x="month", y="sales", markers=True)
trend_fig.update_traces(line_color=TREND_COLOR, marker_color=TREND_COLOR)
trend_fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
style_axes(trend_fig)
st.plotly_chart(trend_fig, width="stretch")

st.divider()

st.subheader("Category and Region Breakdown")
col3, col4 = st.columns(2)

with col3:
    st.write("Sales by Category")
    category_df = sales_by_category(df)
    category_fig = px.bar(
        category_df,
        x="sales",
        y="category",
        orientation="h",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
    )
    category_fig.update_layout(
        xaxis_title="Sales ($)", yaxis_title="Category", showlegend=False
    )
    category_fig.update_yaxes(autorange="reversed")
    style_axes(category_fig)
    st.plotly_chart(category_fig, width="stretch")

with col4:
    st.write("Sales by Region")
    region_df = sales_by_region(df)
    region_fig = px.bar(
        region_df,
        x="sales",
        y="region",
        orientation="h",
        color="region",
        color_discrete_map=REGION_COLORS,
    )
    region_fig.update_layout(
        xaxis_title="Sales ($)", yaxis_title="Region", showlegend=False
    )
    region_fig.update_yaxes(autorange="reversed")
    style_axes(region_fig)
    st.plotly_chart(region_fig, width="stretch")
