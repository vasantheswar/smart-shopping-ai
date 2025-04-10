from app.agents.user_agent import UserAgent
from app.agents.product_agent import ProductAgent
from app.agents.recommender_agent import RecommenderAgent
from datetime import datetime
import sqlite3

class AgentController:
    def __init__(self):
        self.user_agent = UserAgent()
        self.product_agent = ProductAgent()
        self.recommender_agent = RecommenderAgent()
        self.cart = {}  # {user_id: [product_id, ...]}

    def get_user_dashboard(self, user_id):
        profile = self.user_agent.get_user_profile(user_id)
        if not profile:
            return {"error": "User not found."}

        history = self.user_agent.get_user_history(user_id)
        recommendations = self.recommender_agent.get_recommendations(user_id)

        return {
            "profile": profile,
            "recent_activity": history,
            "recommendations": recommendations
        }

    def search_products_by_category(self, category):
        return self.product_agent.get_products_by_category(category)

    def search_products_by_tag(self, subcategory):
        return self.product_agent.get_products_by_subcategory(subcategory)

    def get_random_products(self, limit=5):
        return self.product_agent.get_random_products(limit)

    def add_to_cart(self, user_id, product_id):
        self.cart.setdefault(user_id, []).append(product_id)
        return f"🛒 Product {product_id} added to User {user_id}'s cart."

    def purchase_cart(self, user_id):
        if user_id not in self.cart or not self.cart[user_id]:
            return "🛍️ Cart is empty."

        conn = sqlite3.connect("app/database/smartshop.db")
        cursor = conn.cursor()

        for product_id in self.cart[user_id]:
            cursor.execute("""
                INSERT INTO browsing_history (user_id, product_id, action, timestamp)
                VALUES (?, ?, 'purchased', ?)
            """, (user_id, product_id, datetime.now().isoformat()))

        conn.commit()
        conn.close()

        count = len(self.cart[user_id])
        self.cart[user_id] = []
        return f"✅ Purchased {count} item(s)."
