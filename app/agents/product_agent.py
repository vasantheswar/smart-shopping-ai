import sqlite3

class ProductAgent:
    def __init__(self, db_path="app/database/smartshop.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_product_by_id(self, product_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_recommendation_data WHERE Product_ID = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))

    def get_products_by_category(self, category, limit=10):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM product_recommendation_data 
            WHERE Category = ?
            LIMIT ?
        """, (category, limit))
        products = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return [dict(zip(columns, p)) for p in products]

    def get_products_by_subcategory(self, subcategory, limit=10):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM product_recommendation_data 
            WHERE Subcategory LIKE ?
            LIMIT ?
        """, (f"%{subcategory}%", limit))
        products = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return [dict(zip(columns, p)) for p in products]

    def get_random_products(self, limit=5):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_recommendation_data ORDER BY RANDOM() LIMIT ?", (limit,))
        products = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return [dict(zip(columns, p)) for p in products]
