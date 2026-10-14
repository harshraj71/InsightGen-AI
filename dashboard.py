
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load cleaned dataset
DATA_PATH = Path("data/sales_cleaned.csv")

st.title("📊 Sales Analytics Dashboard")
st.caption("KFC-style sales performance | January–December 2025")

if not DATA_PATH.exists():
    st.error("Dataset not found. Please run analysis.py first.")
    st.stop()

df = pd.read_csv(DATA_PATH)
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df = df.dropna(subset=["Order_Date"])

# Sidebar filters
st.sidebar.header("Filters")

regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

categories = sorted(df["Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters
filtered_df = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        filtered_df["Order_Date"].dt.date.between(
            start_date, end_date
        )
    ]

if filtered_df.empty:
    st.warning("No data matches these filters.")
    st.stop()

# KPI calculations
revenue = filtered_df["Net_Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order_ID"].nunique()
aov = revenue / orders if orders else 0
margin = (profit / revenue * 100) if revenue else 0

# KPI cards
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Revenue", f"₹{revenue:,.2f}")
c2.metric("Total Profit", f"₹{profit:,.2f}")
c3.metric("Unique Orders", f"{orders:,}")
c4.metric("Average Order Value", f"₹{aov:,.2f}")
c5.metric("Profit Margin", f"{margin:.2f}%")

st.divider()

# Monthly sales chart
st.subheader("Monthly Sales Trend")

monthly = (
    filtered_df.groupby(
        filtered_df["Order_Date"].dt.to_period("M")
    )["Net_Sales"]
    .sum()
    .reset_index()
)

monthly["Month"] = monthly["Order_Date"].astype(str)

fig_month = px.line(
    monthly,
    x="Month",
    y="Net_Sales",
    markers=True,
    title="Monthly Net Sales"
)
fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Net Sales (₹)"
)
st.plotly_chart(fig_month, use_container_width=True)

# Category and region charts
left, right = st.columns(2)

with left:
    st.subheader("Revenue by Category")
    category_sales = (
        filtered_df.groupby("Category", as_index=False)
        ["Net_Sales"].sum()
        .sort_values("Net_Sales", ascending=True)
    )

    fig_category = px.bar(
        category_sales,
        x="Net_Sales",
        y="Category",
        orientation="h",
        title="Category Performance"
    )
    st.plotly_chart(fig_category, use_container_width=True)

with right:
    st.subheader("Revenue by Region")
    region_sales = (
        filtered_df.groupby("Region", as_index=False)
        ["Net_Sales"].sum()
        .sort_values("Net_Sales", ascending=False)
    )

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Net_Sales",
        title="Regional Performance"
    )
    st.plotly_chart(fig_region, use_container_width=True)

# Top products
st.subheader("Top 5 Products by Revenue")

top_products = (
    filtered_df.groupby("Product", as_index=False)
    ["Net_Sales"].sum()
    .sort_values("Net_Sales", ascending=False)
    .head(5)
)

st.dataframe(top_products, use_container_width=True, hide_index=True)

# Raw filtered data
with st.expander("View Filtered Sales Data"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.caption("Project built using Python, Pandas, Plotly and Streamlit.")
