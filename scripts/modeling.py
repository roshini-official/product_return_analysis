# ================================
# STEP 1 — Import Libraries
# ================================
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix


# ================================
# STEP 2 — Load Required Datasets
# ================================
orders = pd.read_csv("data/olist_orders_dataset.csv")
order_items = pd.read_csv("data/olist_order_items_dataset.csv")
payments = pd.read_csv("data/olist_order_payments_dataset.csv")
customers = pd.read_csv("data/olist_customers_dataset.csv")


# ================================
# STEP 3 — Create return_flag
# ================================
orders['return_flag'] = orders['order_status'].apply(
    lambda x: 1 if x == 'canceled' else 0
)


# ================================
# STEP 4 — Merge order_items
# ================================
merged_data = order_items.merge(
    orders[['order_id', 'return_flag', 'customer_id']],
    on='order_id',
    how='left'
)


# ================================
# STEP 5 — Convert to Order-Level
# ================================
order_level_data = merged_data.groupby('order_id').agg({
    'price': 'sum',
    'freight_value': 'sum',
    'order_item_id': 'count',
    'return_flag': 'first',
    'customer_id': 'first'
}).reset_index()

order_level_data.rename(columns={
    'price': 'total_price',
    'freight_value': 'total_freight',
    'order_item_id': 'num_items'
}, inplace=True)


# ================================
# STEP 6 — Aggregate Payment Info
# ================================
payment_data = payments.groupby('order_id').agg({
    'payment_installments': 'mean',
    'payment_type': 'first',
    'payment_value': 'sum'
}).reset_index()

order_level_data = order_level_data.merge(
    payment_data,
    on='order_id',
    how='left'
)


# ================================
# STEP 7 — Merge Customer State
# ================================
customer_data = customers[['customer_id', 'customer_state']]

order_level_data = order_level_data.merge(
    customer_data,
    on='customer_id',
    how='left'
)


# ================================
# STEP 8 — Drop Unnecessary Columns
# ================================
order_level_data.drop(columns=['customer_id'], inplace=True)


# ================================
# STEP 9 — Save Final Dataset
# ================================
order_level_data.to_csv("data/final_order_dataset.csv", index=False)
print("Final dataset saved successfully!")


# ================================
# STEP 10 — ML MODEL BUILDING
# ================================

print("\nBuilding Machine Learning Model...")

# Define features and target
X = order_level_data.drop(columns=['order_id', 'return_flag'])
y = order_level_data['return_flag']

# Identify categorical and numerical columns
categorical_cols = ['payment_type', 'customer_state']
numerical_cols = ['total_price', 'total_freight', 'num_items',
                  'payment_installments', 'payment_value']

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'
)

# Create pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000))
])

# Train-test split (stratified because of imbalance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))