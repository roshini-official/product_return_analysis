def product_return_analysis(orders_df, order_items_df, min_orders=10):

    merged = order_items_df.merge(
        orders_df[['order_id', 'return_flag']],
        on='order_id',
        how='left'
    )

    product_stats = merged.groupby('product_id').agg(
        total_orders=('order_id', 'count'),
        total_returns=('return_flag', 'sum')
    ).reset_index()

    product_stats['return_rate'] = (
        product_stats['total_returns'] /
        product_stats['total_orders']
    ) * 100

    product_stats = product_stats[
        product_stats['total_orders'] >= min_orders
    ]

    return product_stats.sort_values(
        by='return_rate',
        ascending=False
    )