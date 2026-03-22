import pandas as pd
# ---------------------------------
# 1️⃣ Return Rate by Product Category
# ---------------------------------
def category_return_rate(orders, order_items, products):

    df = pd.merge(order_items, products, on="product_id", how="left")
    df = pd.merge(df, orders, on="order_id", how="left")

    # Handle column name safely
    if "product_category" in df.columns:
        category_col = "product_category"
    elif "product_category_name" in df.columns:
        category_col = "product_category_name"
    else:
        raise ValueError("No product category column found!")

    category_stats = df.groupby(category_col).agg(
        total_orders=("order_id", "count"),
        total_returns=("is_returned", "sum")
    )

    category_stats["return_rate"] = (
        category_stats["total_returns"] /
        category_stats["total_orders"]
    ) * 100

    return category_stats.sort_values(by="return_rate", ascending=False)


# ---------------------------------
# 2️⃣ Return Reason Distribution
# ---------------------------------
def return_reason_distribution(orders):

    returned_orders = orders[orders["is_returned"] == 1]

    if "return_reason" not in returned_orders.columns:
        return pd.Series(["No return_reason column found"])

    return returned_orders["return_reason"].value_counts()


# ---------------------------------
# 3️⃣ Price vs Return Analysis
# ---------------------------------
def price_return_analysis(orders, order_items):

    df = pd.merge(orders, order_items, on="order_id")

    df["price_range"] = pd.cut(
        df["price"],
        bins=[0, 50, 100, 200, 500, 1000],
        labels=["0-50", "50-100", "100-200", "200-500", "500+"]
    )

    price_stats = df.groupby("price_range").agg(
        total_orders=("order_id", "count"),
        total_returns=("is_returned", "sum")
    )

    price_stats["return_rate"] = (
        price_stats["total_returns"] /
        price_stats["total_orders"]
    ) * 100

    return price_stats