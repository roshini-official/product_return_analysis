import streamlit as st
import pandas as pd

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

# --------------------------------
# Page Setup
# --------------------------------

st.set_page_config(page_title="E-Commerce Return Dashboard", layout="wide")

st.title("📦 E-Commerce Return Analysis Dashboard")

st.markdown(
"""
This dashboard analyzes **product return behavior, financial loss,
and root causes of product returns**.
"""
)

# --------------------------------
# Load Data
# --------------------------------

data_path = "data"

datasets = load_datasets(data_path)

orders = datasets['orders']
order_items = datasets['order_items']
customers = datasets['customers']

# --------------------------------
# Preprocess Orders
# --------------------------------

orders = preprocess_orders(orders)

# --------------------------------
# KPI METRICS
# --------------------------------

total_orders = len(orders)
total_returns = orders["is_returned"].sum()
return_rate = (total_returns / total_orders) * 100

total_loss = calculate_financial_loss(orders, order_items)

st.subheader("📊 Business Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", total_orders)
col2.metric("Returned Orders", total_returns)
col3.metric("Return Rate", f"{return_rate:.2f}%")
col4.metric("Financial Loss", f"${total_loss:,.2f}")

st.markdown("---")

# --------------------------------
# Product Return Analysis
# --------------------------------

st.header("📦 Frequently Returned Products")

product_stats = product_return_analysis(orders, order_items)

st.dataframe(product_stats.head(10))

st.bar_chart(product_stats.head(10)["return_rate"])

st.markdown("---")

# --------------------------------
# Root Cause Analysis
# --------------------------------

st.header("🔍 Root Cause Analysis")

# Category Return Rate
st.subheader("Return Rate by Category")

category_analysis = category_return_rate(orders, order_items)

st.dataframe(category_analysis.head(10))

st.bar_chart(category_analysis.head(10)["return_rate"])

# Return Reason Distribution
st.subheader("Return Reason Distribution")

reason_analysis = return_reason_distribution(orders)

st.dataframe(reason_analysis)

st.bar_chart(reason_analysis)

# Price vs Return Analysis
st.subheader("Price vs Return Analysis")

price_analysis = price_return_analysis(orders, order_items)

st.dataframe(price_analysis.head(10))

st.line_chart(price_analysis["return_rate"])

st.markdown("---")

# --------------------------------
# Customer Region Analysis
# --------------------------------

st.header("🌎 Customer Region Return Analysis")

state_analysis = customer_region_analysis(orders, customers)

st.dataframe(state_analysis.head(10))

st.bar_chart(state_analysis.head(10)["return_rate"])

st.markdown("---")

# --------------------------------
# Business Insights
# --------------------------------

st.header("📌 Key Insights")

top_category = category_analysis.index[0]
top_rate = category_analysis["return_rate"].iloc[0]

st.success(
    f"Highest return rate category: **{top_category} ({top_rate:.2f}%)**"
)

top_state = state_analysis.index[0]
state_rate = state_analysis["return_rate"].iloc[0]

st.info(
    f"State with highest return rate: **{top_state} ({state_rate:.2f}%)**"
)

st.warning(
    "Products with higher prices and delayed shipping tend to have higher return rates."
)

st.markdown("---")

st.caption("Dashboard generated using Python, Pandas, and Streamlit.")