def calculate_financial_loss(orders_df, order_items_df):

    merged = order_items_df.merge(
        orders_df[['order_id', 'return_flag']],
        on='order_id',
        how='left'
    )

    merged['total_loss'] = (
        (merged['price'] + merged['freight_value'])
        * merged['return_flag']
    )

    total_loss = merged['total_loss'].sum()

    return total_loss