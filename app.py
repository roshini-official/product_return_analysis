import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Return Analysis Dashboard", layout="wide")

st.title("📦 E-Commerce Product Return Analysis Dashboard")

st.write("Upload datasets to analyze product returns and financial loss.")

orders_file = st.file_uploader("Upload Orders Dataset", type=["csv"])
items_file = st.file_uploader("Upload Order Items Dataset", type=["csv"])
products_file = st.file_uploader("Upload Products Dataset", type=["csv"])
translation_file = st.file_uploader("Upload Category Translation Dataset", type=["csv"])

if orders_file and items_file and products_file and translation_file:

    orders = pd.read_csv(orders_file)
    items = pd.read_csv(items_file)
    products = pd.read_csv(products_file)
    translation = pd.read_csv(translation_file)

    products = pd.merge(products, translation, on="product_category_name", how="left")

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    # -------------------------------
    # BASIC METRICS
    # -------------------------------

    total_orders = len(orders)

    returned_orders = orders[orders["order_status"] == "canceled"]

    total_returns = len(returned_orders)

    return_rate = (total_returns / total_orders) * 100

    cancelled_items = pd.merge(returned_orders, items, on="order_id")
    cancelled_items = pd.merge(cancelled_items, products, on="product_id")

    total_loss = cancelled_items["price"].sum()

    st.header("📊 Key Business Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", total_orders)
    col2.metric("Returned Orders", total_returns)
    col3.metric("Return Rate", f"{return_rate:.2f}%")
    col4.metric("Financial Loss", f"${total_loss:,.2f}")

    # -------------------------------
    # DATA PREVIEW
    # -------------------------------

    st.subheader("Dataset Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Orders")
        st.dataframe(orders.head())

    with col2:
        st.write("Order Items")
        st.dataframe(items.head())

    # -------------------------------
    # TOP RETURNED PRODUCTS
    # -------------------------------

    st.header("📦 Frequently Returned Product Categories")

    top_products = (
        cancelled_items["product_category_name_english"]
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots()

    ax.barh(top_products.index, top_products.values)

    plt.title("Top Returned Product Categories")

    st.pyplot(fig)

    # -------------------------------
    # MONTHLY RETURN TREND
    # -------------------------------

    st.header("📈 Monthly Return Trend")

    returned_orders["order_month"] = (
        returned_orders["order_purchase_timestamp"].dt.to_period("M")
    )

    monthly_returns = returned_orders.groupby("order_month").size()

    st.line_chart(monthly_returns)

    # -------------------------------
    # ROOT CAUSE ANALYSIS
    # -------------------------------

    st.header("🔎 Root Cause Analysis")

    merged_df = pd.merge(orders, items, on="order_id")
    merged_df = pd.merge(merged_df, products, on="product_id")

    merged_df["is_returned"] = merged_df["order_status"] == "canceled"

    # Return rate by category

    st.subheader("Return Rate by Category")

    category_analysis = merged_df.groupby(
        "product_category_name_english"
    ).agg(
        total_orders=("order_id", "count"),
        total_returns=("is_returned", "sum")
    )

    category_analysis["return_rate"] = (
        category_analysis["total_returns"] /
        category_analysis["total_orders"]
    ) * 100

    category_analysis = category_analysis.sort_values(
        "return_rate", ascending=False
    ).head(10)

    fig1, ax1 = plt.subplots()

    ax1.bar(category_analysis.index, category_analysis["return_rate"])

    plt.xticks(rotation=45)

    st.pyplot(fig1)

    # -------------------------------
    # SHIPPING DELAY ANALYSIS
    # -------------------------------

    st.subheader("Shipping Delay vs Return Rate")

    orders["order_delivered_customer_date"] = pd.to_datetime(
        orders["order_delivered_customer_date"]
    )

    orders["shipping_delay"] = (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
    ).dt.days

    delay_analysis = orders.groupby("shipping_delay").agg(
        orders=("order_id", "count"),
        returns=("order_status", lambda x: (x == "canceled").sum())
    )

    delay_analysis["return_rate"] = (
        delay_analysis["returns"] /
        delay_analysis["orders"]
    ) * 100

    fig4, ax4 = plt.subplots()

    ax4.plot(delay_analysis.index, delay_analysis["return_rate"])

    st.pyplot(fig4)

else:

    st.info("Upload all datasets to run the analysis.")