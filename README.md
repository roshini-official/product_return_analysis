📦 Product Return Analysis

Overview
This project analyzes product return data to understand trends, reasons for returns, and patterns across products and categories. The goal is to provide actionable insights to help reduce return rates and improve business decisions.

📍 Table of Contents

Project Overview

Dataset

Analysis Workflow

How to Run

Results & Visualizations

Tools & Dependencies

Insights & Conclusions

Future Work

License

🚀 Project Overview

This repository performs exploratory data analysis (EDA) on product return data to:

Identify products and categories with high return rates

Understand key factors leading to returns

Visualize trends and patterns in returns over time

The analysis can support data-driven decisions to reduce product returns.

🧾 Dataset

Source: Olist e-commerce public datasets

Format: CSV files

Key Columns:

order_id – unique identifier for each order

return_flag – indicates whether an order was returned

product_category – category of the product

review_score – customer review score

order_purchase_timestamp – date of purchase

Data cleaning and preprocessing were applied to handle missing values and standardize formats.

🔍 Analysis Workflow

Data Loading & Cleaning: load CSVs and handle missing/duplicate data

Exploratory Data Analysis (EDA): visualize return patterns, review scores, and product categories

Feature Analysis: investigate factors that may influence returns

Visualization: generate plots for insights using matplotlib and seaborn

⚙️ How to Run
# Clone the repository
git clone https://github.com/roshini-official/product_return_analysis.git

# Navigate to the project directory
cd product_return_analysis

# Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run analysis scripts or Jupyter notebooks
jupyter notebook
📊 Results & Visualizations

Boxplots comparing review scores for returned vs non-returned products

Category-wise return distribution charts

Time-series trends for returns

Add screenshots or .png files of your key visualizations for clarity.

🛠️ Tools & Dependencies

Python 3.x

pandas, numpy, matplotlib, seaborn

Jupyter Notebook

🧠 Insights & Conclusions

Certain product categories have higher return rates

Products with lower review scores are more likely to be returned

Seasonality may affect return patterns

📌 Future Work

Apply machine learning to predict likely returns

Build an interactive dashboard for real-time insights

Integrate more datasets for deeper analysis

📄 License

This project is licensed under the MIT License.
