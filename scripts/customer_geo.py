def customer_region_analysis(orders_df, customers_df):

    merged = orders_df.merge(
        customers_df[['customer_id', 'customer_state']],
        on='customer_id',
        how='left'
    )

    state_stats = merged.groupby('customer_state').agg(
        total_orders=('order_id', 'count'),
        total_returns=('return_flag', 'sum')
    ).reset_index()

    state_stats['return_rate_%'] = (
        state_stats['total_returns'] /
        state_stats['total_orders']
    ) * 100

    return state_stats.sort_values(
        by='return_rate_%',
        ascending=False
    )