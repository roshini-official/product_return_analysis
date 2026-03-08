import os
import pandas as pd

def safe_load_csv(file_path):
    """
    Safely load a CSV file. Returns None if the file is missing.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: File not found: {file_path}. Skipping this dataset.")
        return None
    df = pd.read_csv(file_path)
    print(f"✅ Loaded '{os.path.basename(file_path)}' successfully. Shape: {df.shape}")
    return df

def load_datasets():
    """
    Load all Olist datasets safely.
    Skips any missing files instead of raising an error.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(script_dir, '..', 'data')

    files = {
        'customers': 'olist_customers_dataset.csv',
        'orders': 'olist_orders_dataset.csv',
        'order_items': 'olist_order_items_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'reviews': 'olist_order_reviews_dataset.csv',
        'sellers': 'olist_sellers_dataset.csv',
        'payments': 'olist_order_payments_dataset.csv',
        'category_translation': 'product_category_name_translation.csv',
        'final_dataset': 'final_dataset.csv'  # will skip if missing
    }

    datasets = {}
    for key, filename in files.items():
        file_path = os.path.join(data_folder, filename)
        df = safe_load_csv(file_path)
        if df is not None:
            datasets[key] = df

    return datasets

def main():
    print("Loading datasets...")
    datasets = load_datasets()
    print("\nAll available datasets loaded successfully!")

    # Example: Accessing a dataset
    if 'customers' in datasets:
        print("\nCustomers dataset head:")
        print(datasets['customers'].head())

if __name__ == "__main__":
    main()