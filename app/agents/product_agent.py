import sqlite3
import os

class ProductAgent:
    def __init__(self, db_path=None):
        # Set default DB path if not provided
        self.db_path = db_path or os.path.join("app", "database", "smartshop.db")

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_product_by_id(self, product_id):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM product_recommendation_data WHERE Product_ID = ?", (product_id,))
            row = cursor.fetchone()
            if not row:
                return None
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        finally:
            conn.close()

    def get_products_by_category(self, category, limit=10):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM product_recommendation_data 
                WHERE Category = ?
                LIMIT ?
            """, (category, limit))
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, p)) for p in products]
        finally:
            conn.close()

    def get_products_by_subcategory(self, subcategory, limit=10):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM product_recommendation_data 
                WHERE Subcategory LIKE ?
                LIMIT ?
            """, (f"%{subcategory}%", limit))
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, p)) for p in products]
        finally:
            conn.close()

    def get_random_products(self, limit=5):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM product_recommendation_data 
                ORDER BY RANDOM() 
                LIMIT ?
            """, (limit,))
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, p)) for p in products]
        finally:
            conn.close()
