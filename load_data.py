import pandas as pd
import sqlite3
import os

# Paths
db_path = "app/database/smartshop.db"
customer_csv = "data/customer_data_collection.csv"
product_csv = "data/product_recommendation_data.csv"

# Load CSVs
customer_df = pd.read_csv(customer_csv)
product_df = pd.read_csv(product_csv)

# Connect to DB
conn = sqlite3.connect(db_path)

# Load data into tables
customer_df.to_sql("customer_data_collection", conn, if_exists="replace", index=False)
product_df.to_sql("product_recommendation_data", conn, if_exists="replace", index=False)

conn.close()
print("✅ Data loaded successfully into the SQLite database.")
