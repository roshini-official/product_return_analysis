import pandas as pd


# ---------------------------------
# 1️⃣ Return Rate by Product Category
# ---------------------------------
def category_return_rate(orders, order_items):

    # Merge orders and order items
    df = pd.merge(orders, order_items, on="order_id")

    # Group by product category
    category_stats = df.groupby("product_category").agg(
        total_orders=("order_id", "count"),
        total_returns=("is_returned", "sum")
    )

    # Calculate return rate
    category_stats["return_rate"] = (
        category_stats["total_returns"] /
        category_stats["total_orders"]
    ) * 100

    # Sort by highest return rate
    category_stats = category_stats.sort_values(
        "return_rate", ascending=False
    )

    return category_stats


# ---------------------------------
# 2️⃣ Return Reason Distribution
# ---------------------------------
def return_reason_distribution(orders):

    # Filter only returned orders
    returned_orders = orders[orders["is_returned"] == 1]

    # Count return reasons
    reason_stats = returned_orders["return_reason"].value_counts()

    return reason_stats


# ---------------------------------
# 3️⃣ Price vs Return Analysis
# ---------------------------------
def price_return_analysis(orders, order_items):

    # Merge datasets
    df = pd.merge(orders, order_items, on="order_id")

    # Create price bins
    df["price_range"] = pd.cut(
        df["price"],
        bins=[0, 50, 100, 200, 500, 1000],
        labels=["0-50", "50-100", "100-200", "200-500", "500+"]
    )

    # Group by price range
    price_stats = df.groupby("price_range").agg(
        total_orders=("order_id", "count"),
        total_returns=("is_returned", "sum")
    )

    # Calculate return rate
    price_stats["return_rate"] = (
        price_stats["total_returns"] /
        price_stats["total_orders"]
    ) * 100

    return price_stats