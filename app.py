import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Return Analysis Dashboard", layout="wide")

st.title("📦 E-Commerce Product Return Analysis Dashboard")

st.write("Upload datasets to analyze product returns, return rates, and financial loss.")

# -----------------------------
# FILE UPLOAD
# -----------------------------

orders_file = st.file_uploader("Upload Orders Dataset", type=["csv"])
items_file = st.file_uploader("Upload Order Items Dataset", type=["csv"])
products_file = st.file_uploader("Upload Products Dataset", type=["csv"])
translation_file = st.file_uploader("Upload Category Translation Dataset", type=["csv"])

if orders_file and items_file and products_file and translation_file:

    # -----------------------------
    # LOAD DATA
    # -----------------------------

    orders = pd.read_csv(orders_file)
    items = pd.read_csv(items_file)
    products = pd.read_csv(products_file)
    translation = pd.read_csv(translation_file)

    # Merge category translation
    products = pd.merge(products, translation, on="product_category_name", how="left")

    # Convert dates
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    # Merge datasets
    merged_df = pd.merge(orders, items, on="order_id")
    merged_df = pd.merge(merged_df, products, on="product_id")

    merged_df["is_returned"] = merged_df["order_status"] == "canceled"

    # -----------------------------
    # SIDEBAR FILTERS
    # -----------------------------

    st.sidebar.header("🔎 Dashboard Filters")

    category_filter = st.sidebar.selectbox(
        "Select Product Category",
        ["All"] + list(merged_df["product_category_name_english"].dropna().unique())
    )

    if category_filter != "All":
        merged_df = merged_df[
            merged_df["product_category_name_english"] == category_filter
        ]

    # -----------------------------
    # KPI METRICS
    # -----------------------------

    total_orders = merged_df["order_id"].nunique()

    total_returns = merged_df[merged_df["is_returned"]]["order_id"].nunique()

    return_rate = (total_returns / total_orders) * 100 if total_orders != 0 else 0

    total_loss = merged_df[merged_df["is_returned"]]["price"].sum()

    st.header("📊 Key Business Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", total_orders)
    col2.metric("Returned Orders", total_returns)
    col3.metric("Return Rate", f"{return_rate:.2f}%")
    col4.metric("Financial Loss", f"${total_loss:,.2f}")

    # -----------------------------
    # MONTHLY RETURN TREND
    # -----------------------------

    st.header("📈 Monthly Return Trend")

    merged_df["order_month"] = (
        merged_df["order_purchase_timestamp"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_orders = merged_df.groupby("order_month")["order_id"].nunique()

    monthly_returns = merged_df[merged_df["is_returned"]].groupby(
        "order_month"
    )["order_id"].nunique()

    trend_df = pd.DataFrame({
        "orders": monthly_orders,
        "returns": monthly_returns
    }).fillna(0)

    trend_df["return_rate"] = (trend_df["returns"] / trend_df["orders"]) * 100

    fig = px.line(
        trend_df,
        x=trend_df.index,
        y="return_rate",
        title="Monthly Return Rate Trend",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # TOP RETURNED CATEGORIES
    # -----------------------------

    st.header("📦 Top Returned Product Categories")

    category_returns = (
        merged_df[merged_df["is_returned"]]
        .groupby("product_category_name_english")
        .size()
        .reset_index(name="returns")
        .sort_values("returns", ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        category_returns,
        x="returns",
        y="product_category_name_english",
        orientation="h",
        title="Top 10 Returned Categories"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # TOP PRODUCTS CAUSING LOSS
    # -----------------------------

    st.header("💰 Products Causing Highest Financial Loss")

    loss_products = merged_df[merged_df["is_returned"]].groupby(
        "product_id"
    ).agg(
        total_returns=("order_id", "count"),
        revenue_loss=("price", "sum")
    ).sort_values("revenue_loss", ascending=False).head(10)

    st.dataframe(loss_products)

    # -----------------------------
    # SHIPPING DELAY ANALYSIS
    # -----------------------------

    st.header("🚚 Shipping Delay vs Return Rate")

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
        delay_analysis["returns"] / delay_analysis["orders"]
    ) * 100

    fig3 = px.line(
        delay_analysis,
        x=delay_analysis.index,
        y="return_rate",
        title="Shipping Delay Impact on Return Rate"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -----------------------------
    # DATA PREVIEW
    # -----------------------------

    if st.checkbox("Show Raw Data"):
        st.subheader("Merged Dataset")
        st.dataframe(merged_df)

    # -----------------------------
    # BUSINESS INSIGHTS
    # -----------------------------

    st.header("📌 Key Insights")

    st.markdown("""
    - Some product categories show significantly higher return rates.
    - Longer shipping delays tend to increase return probability.
    - A small number of products contribute heavily to financial loss.
    - Monitoring monthly return trends helps detect operational issues.
    """)

else:

    st.info("Upload all datasets to start the dashboard.")