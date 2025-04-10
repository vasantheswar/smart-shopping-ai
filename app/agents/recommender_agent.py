import sqlite3
import pandas as pd

class RecommenderAgent:
    def __init__(self, db_path="app/database/smartshop.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_recommendations(self, user_id=None, top_n=5):
        """
        Returns top N recommended products based on highest
        probability of recommendation and product rating.
        """
        conn = self.connect()
        query = """
        SELECT * FROM product_recommendation_data
        WHERE Probability_of_Recommendation > 0.7
        ORDER BY Product_Rating DESC, Probability_of_Recommendation DESC
        LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(top_n,))
        conn.close()
        return df.to_dict(orient="records")
