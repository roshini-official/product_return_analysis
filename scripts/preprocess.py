import pandas as pd
def preprocess_orders(orders_df):
    """
    Add return_flag and process date columns.
    """
    orders_df['return_flag'] = orders_df['order_status'].apply(
        lambda x: 1 if x in ['canceled', 'unavailable'] else 0
    )

    orders_df['order_purchase_timestamp'] = pd.to_datetime(
        orders_df['order_purchase_timestamp']
    )

    orders_df['year_month'] = (
        orders_df['order_purchase_timestamp']
        .dt.to_period('M')
        .astype(str)
    )

    return orders_df