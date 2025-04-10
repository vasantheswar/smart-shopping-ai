import sqlite3

conn = sqlite3.connect("app/database/smartshop.db")
cursor = conn.cursor()

print("Tables:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

print("\nCustomer Table Schema:")
cursor.execute("PRAGMA table_info(customer_data_collection)")
columns = cursor.fetchall()
for col in columns:
    print(col)

print("\nSample Data:")
cursor.execute("SELECT * FROM customer_data_collection LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
