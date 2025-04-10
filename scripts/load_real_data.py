import sqlite3
import pandas as pd
import os

# Set paths
DB_PATH = "app/database/smartshop.db"
CUSTOMER_CSV = "data/customer_data_collection.csv"
PRODUCT_CSV = "data/product_recommendation_data.csv"

# Load CSVs into DataFrames
print("📦 Loading CSVs...")
customers = pd.read_csv(CUSTOMER_CSV)
products = pd.read_csv(PRODUCT_CSV)

# Standardize column names
customers.columns = [col.strip().replace(" ", "_") for col in customers.columns]
products.columns = [col.strip().replace(" ", "_") for col in products.columns]

# Create database folder if not exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect and insert
conn = sqlite3.connect(DB_PATH)
print("🧠 Writing to SQLite DB...")
customers.to_sql("customer_data_collection", conn, if_exists="replace", index=False)
products.to_sql("product_recommendation_data", conn, if_exists="replace", index=False)
conn.close()

print("✅ Database successfully created at", DB_PATH)
