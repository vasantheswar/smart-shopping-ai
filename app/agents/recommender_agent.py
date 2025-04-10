import sqlite3
import pandas as pd
import os

class RecommenderAgent:
    def __init__(self, db_path=None):
        # Use default relative path suitable for both local and cloud environments
        self.db_path = db_path or os.path.join("app", "database", "smartshop.db")

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_recommendations(self, user_id=None, top_n=5):
        """
        Returns top N recommended products based on:
        - High Probability of Recommendation (> 0.7)
        - High Product Rating (sorted descending)
        """
        try:
            conn = self.connect()
            query = """
                SELECT * FROM product_recommendation_data
                WHERE Probability_of_Recommendation > 0.7
                ORDER BY Product_Rating DESC, Probability_of_Recommendation DESC
                LIMIT ?
            """
            df = pd.read_sql_query(query, conn, params=(top_n,))
            return df.to_dict(orient="records")
        except Exception as e:
            return [{"error": f"Failed to fetch recommendations: {e}"}]
        finally:
            if conn:
                conn.close()
