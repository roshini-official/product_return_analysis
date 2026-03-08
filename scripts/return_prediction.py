import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import RandomOverSampler

# -----------------------------
# 1. Load Datasets
# -----------------------------
orders = pd.read_csv(r'C:\product_return_analysis\data\olist_orders_dataset.csv')
order_items = pd.read_csv(r'C:\product_return_analysis\data\olist_order_items_dataset.csv')
customers = pd.read_csv(r'C:\product_return_analysis\data\olist_customers_dataset.csv')
reviews = pd.read_csv(r'C:\product_return_analysis\data\olist_order_reviews_dataset.csv')

# -----------------------------
# 2. Merge Main Tables
# -----------------------------
data = orders.merge(order_items, on='order_id', how='left') \
             .merge(customers, on='customer_id', how='left') \
             .merge(reviews, on='order_id', how='left')

# -----------------------------
# 3. Create Simulated Return Flag
# -----------------------------
# We assume low review score => likely return
data['return_flag'] = data['review_score'].apply(lambda x: 1 if x <= 2 else 0)

print("Simulated return distribution:\n", data['return_flag'].value_counts())

# -----------------------------
# 4. Prepare Features
# -----------------------------
features = ['order_purchase_timestamp', 'order_approved_at', 'price', 'freight_value', 'review_score']
X = data[features].copy()

# Handle timestamps
for col in ['order_purchase_timestamp','order_approved_at']:
    X[col] = pd.to_datetime(X[col], errors='coerce')
    X[col] = X[col].fillna(X[col].median())
    X[col] = X[col].astype(int) // 10**9

X.fillna(0, inplace=True)
y = data['return_flag']

# -----------------------------
# 5. Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 6. Oversampling
# -----------------------------
ros = RandomOverSampler(random_state=42)
X_train_res, y_train_res = ros.fit_resample(X_train, y_train)

print("Oversampled distribution:\n", pd.Series(y_train_res).value_counts())

# -----------------------------
# 7. Train Random Forest
# -----------------------------
rf = RandomForestClassifier(
    n_estimators=200,
    class_weight='balanced',
    random_state=42
)
rf.fit(X_train_res, y_train_res)

# -----------------------------
# 8. Predictions
# -----------------------------
y_pred = rf.predict(X_test)

# -----------------------------
# 9. Evaluation
# -----------------------------
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -----------------------------
# 10. Feature Importance
# -----------------------------
feat_imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature Importance:\n", feat_imp)