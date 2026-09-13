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

st.subheader("Sales Trend Over Time")
monthly = monthly_sales(df)
trend_fig = px.line(monthly, x="month", y="sales", markers=True)
trend_fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
st.plotly_chart(trend_fig, use_container_width=True)

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
