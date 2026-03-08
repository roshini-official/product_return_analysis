import pandas as pd

def load_datasets(data_path):
    datasets = {}
    datasets['customers'] = pd.read_csv(f"{data_path}/olist_customers_dataset.csv")
    datasets['orders'] = pd.read_csv(f"{data_path}/olist_orders_dataset.csv")
    datasets['order_items'] = pd.read_csv(f"{data_path}/olist_order_items_dataset.csv")
    datasets['products'] = pd.read_csv(f"{data_path}/olist_products_dataset.csv")
    datasets['reviews'] = pd.read_csv(f"{data_path}/olist_order_reviews_dataset.csv")
    datasets['sellers'] = pd.read_csv(f"{data_path}/olist_sellers_dataset.csv")
    datasets['payments'] = pd.read_csv(f"{data_path}/olist_order_payments_dataset.csv")
    datasets['category_translation'] = pd.read_csv(f"{data_path}/product_category_name_translation.csv")
    return datasets