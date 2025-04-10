import sqlite3
import os

class UserAgent:
    def __init__(self, db_path=None):
        # Use relative path so it works on both local and cloud
        self.db_path = db_path or os.path.join("app", "database", "smartshop.db")

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_user_profile(self, user_id):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Check that Customer_ID column exists
            cursor.execute("PRAGMA table_info(customer_data_collection)")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]

            if "Customer_ID" not in column_names:
                raise ValueError("Customer_ID column not found in table. Check the CSV structure.")

            cursor.execute("SELECT * FROM customer_data_collection WHERE Customer_ID = ?", (user_id,))
            user = cursor.fetchone()

            if not user:
                return None

            columns = [desc[0] for desc in cursor.description]
            user_data = dict(zip(columns, user))
            return user_data

        except Exception as e:
            return {"error": f"User profile query failed: {e}"}

        finally:
            if conn:
                conn.close()

    def get_user_history(self, user_id):
        profile = self.get_user_profile(user_id)
        if not profile or isinstance(profile, dict) and profile.get("error"):
            return []

        return {
            "Browsing History": profile.get("Browsing_History", ""),
            "Purchase History": profile.get("Purchase_History", "")
        }
