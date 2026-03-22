import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Import modules
from scripts.load_data import load_datasets
from scripts.preprocess import preprocess_orders
from scripts.analysis import product_return_analysis
from scripts.financials import calculate_financial_loss
from scripts.customer_geo import customer_region_analysis
from scripts.root_cause_analysis import (
    category_return_rate,
    return_reason_distribution,
    price_return_analysis
)

# -------------------------------------------------------
# Page Setup
# -------------------------------------------------------
st.set_page_config(page_title="E-Commerce Return Dashboard", layout="wide")

st.title("📦 E-Commerce Return Analysis Dashboard")

st.markdown("""
This dashboard analyzes **product return behavior, financial loss,
and root causes of product returns**.
""")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------
data_path = Path("data")
datasets = load_datasets(str(data_path))

orders = datasets['orders']
order_items = datasets['order_items']
customers = datasets['customers']
products = datasets['products']

orders = preprocess_orders(orders)

# -------------------------------------------------------
# Ensure return column exists
# -------------------------------------------------------
if "is_returned" not in orders.columns:
    if "order_status" in orders.columns:
        orders["is_returned"] = (orders["order_status"] == "canceled").astype(int)
    else:
        orders["is_returned"] = 0

# -------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------
st.sidebar.header("🔎 Filters")

# Date filter
if "order_purchase_timestamp" in orders.columns:
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    min_date = orders["order_purchase_timestamp"].min().date()
    max_date = orders["order_purchase_timestamp"].max().date()

    date_range = st.sidebar.date_input("📅 Date Range", value=[min_date, max_date])

    if len(date_range) == 2:
        orders = orders[
            (orders["order_purchase_timestamp"].dt.date >= date_range[0]) &
            (orders["order_purchase_timestamp"].dt.date <= date_range[1])
        ]

# Category filter (robust)
merged = orders.merge(order_items, on="order_id", how="left")
merged = merged.merge(products, on="product_id", how="left")

category_col = None
for col in merged.columns:
    if "category" in col.lower():
        category_col = col
        break

if category_col:
    categories = sorted(merged[category_col].dropna().unique())

    selected_categories = st.sidebar.multiselect(
        "📦 Product Category",
        options=categories,
        default=categories[:10] if len(categories) > 10 else categories
    )

    if selected_categories:
        valid_orders = merged[
            merged[category_col].isin(selected_categories)
        ]["order_id"].unique()

        orders = orders[orders["order_id"].isin(valid_orders)]

# -------------------------------------------------------
# KPI METRICS
# -------------------------------------------------------
total_orders = len(orders)
total_returns = orders["is_returned"].sum()
return_rate = (total_returns / total_orders) * 100 if total_orders > 0 else 0
total_loss = calculate_financial_loss(orders, order_items)

st.subheader("📊 Business Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Returned Orders", f"{int(total_returns):,}")
col3.metric("Return Rate", f"{return_rate:.2f}%")
col4.metric("Financial Loss", f"${total_loss:,.2f}")

st.markdown("---")

# -------------------------------------------------------
# PRODUCT RETURN ANALYSIS
# -------------------------------------------------------
st.header("📦 Frequently Returned Products")

product_stats = product_return_analysis(orders, order_items)
top_products = product_stats.head(10).reset_index()

# Detect return rate column
rate_col = next((c for c in top_products.columns if "return" in c.lower()), None)
id_col = next((c for c in top_products.columns if "product" in c.lower()), top_products.columns[0])

fig_products = px.bar(
    top_products,
    x=id_col,
    y=rate_col,
    color=rate_col,
    title="Top 10 Products by Return Rate",
    text_auto=".2f"
)

st.plotly_chart(fig_products, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------
# ROOT CAUSE ANALYSIS
# -------------------------------------------------------
st.header("🔍 Root Cause Analysis")

col1, col2 = st.columns(2)

# Category Analysis
with col1:
    st.subheader("Return Rate by Category")

    category_analysis = category_return_rate(orders, order_items, products)
    cat_df = category_analysis.head(10).reset_index()

    rate_col = next((c for c in cat_df.columns if "return" in c.lower()), None)
    cat_col = cat_df.columns[0]

    fig_cat = px.bar(
        cat_df,
        x=rate_col,
        y=cat_col,
        orientation="h",
        color=rate_col,
        title="Top Categories by Return Rate",
        text_auto=".2f"
    )

    st.plotly_chart(fig_cat, use_container_width=True)

# Return Reason
with col2:
    st.subheader("Return Reason Distribution")

    reason_analysis = return_reason_distribution(orders)

    fig_reason = px.pie(
        names=reason_analysis.index,
        values=reason_analysis.values,
        title="Return Reasons"
    )

    st.plotly_chart(fig_reason, use_container_width=True)

# Price Analysis
st.subheader("Price vs Return Rate")

price_analysis = price_return_analysis(orders, order_items)
price_df = price_analysis.reset_index()

rate_col = next((c for c in price_df.columns if "return" in c.lower()), None)

fig_price = px.line(
    price_df,
    x=price_df.columns[0],
    y=rate_col,
    title="Return Rate by Price Range"
)

st.plotly_chart(fig_price, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------
# CUSTOMER REGION ANALYSIS
# -------------------------------------------------------
st.header("🌎 Customer Region Analysis")

state_analysis = customer_region_analysis(orders, customers)
state_df = state_analysis.head(10).reset_index()

rate_col = next((c for c in state_df.columns if "return" in c.lower()), None)
state_col = next((c for c in state_df.columns if "state" in c.lower()), state_df.columns[0])

fig_state = px.bar(
    state_df,
    x=state_col,
    y=rate_col,
    color=rate_col,
    title="Top States by Return Rate",
    text_auto=".2f"
)

st.plotly_chart(fig_state, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------
# INSIGHTS
# -------------------------------------------------------
st.header("📌 Key Insights")

try:
    top_category = category_analysis.index[0]
    top_rate = category_analysis.iloc[0][rate_col]
    st.success(f"🏆 Highest return category: {top_category} ({top_rate:.2f}%)")
except:
    pass

try:
    top_state = state_analysis.index[0]
    state_rate = state_analysis.iloc[0][rate_col]
    st.info(f"📍 Highest return state: {top_state} ({state_rate:.2f}%)")
except:
    pass

st.markdown("---")
st.caption("Built with Streamlit · Pandas · Plotly")