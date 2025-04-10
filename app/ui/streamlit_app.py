import sys
import os
import sqlite3
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.main import AgentController

st.set_page_config(page_title="Smart Shopping AI", layout="wide")
st.markdown("""
    <style>
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-size: 1.1rem;
    }
    h2 { font-size: 28px !important; }
    .product-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        font-size: 18px;
    }
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Smart Shopping - Personalized E-Commerce")
controller = AgentController()

# Sidebar user selection
st.sidebar.header("User Settings")
try:
    conn = sqlite3.connect("app/database/smartshop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Customer_ID, Customer_Name FROM customer_data_collection LIMIT 100")
    rows = cursor.fetchall()
    available_users = [f"{row[0]} - {row[1]}" for row in rows]
    user_map = {f"{row[0]} - {row[1]}": row[0] for row in rows}
    conn.close()
except:
    available_users = ["C1000 - Unknown"]
    user_map = {"C1000 - Unknown": "C1000"}

selected_user = st.sidebar.selectbox("Select User", available_users)
user_id = user_map[selected_user]

# Search
search_type = st.sidebar.selectbox("Search By", ["Category", "Subcategory"])
query = st.sidebar.text_input("Enter search term")

# Tabs
dashboard_tab, cart_tab = st.tabs(["Dashboard", "Cart"])

with dashboard_tab:
    dashboard = controller.get_user_dashboard(user_id)
    if "error" in dashboard:
        st.error(dashboard["error"])
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("User Profile")
            st.json(dashboard["profile"])
        with col2:
            st.subheader("User History")
            st.json(dashboard["recent_activity"])

        st.subheader("Recommended Products")
        st.markdown("<div class='product-grid'>", unsafe_allow_html=True)
        for rec in dashboard["recommendations"]:
            st.markdown(f"""
                <div class='product-card'>
                    <strong>{rec.get('Brand', 'Product')}</strong> - ₹{rec.get('Price', 'N/A')}<br>
                    Category: {rec.get('Category', '')}<br>
                    Subcategory: {rec.get('Subcategory', '')}
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if query:
            st.subheader(f"Search Results for '{query}' ({search_type})")
            results = (
                controller.search_products_by_category(query)
                if search_type == "Category"
                else controller.search_products_by_tag(query)
            )
            if results:
                st.markdown("<div class='product-grid'>", unsafe_allow_html=True)
                for p in results:
                    st.markdown(f"""
                        <div class='product-card'>
                            <strong>{p['Brand']}</strong> - ₹{p['Price']}<br>
                            Category: {p['Category']}<br>
                            Subcategory: {p['Subcategory']}
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No results found.")

with cart_tab:
    st.subheader("Your Shopping Cart")
    all_products = controller.get_random_products(limit=20)
    product_options = {f"{p['Brand']} - ₹{p['Price']}": p["Product_ID"] for p in all_products}

    col1, col2 = st.columns(2)
    with col1:
        selected = st.selectbox("Choose a product to add", list(product_options.keys()))
    with col2:
        if st.button("Add to Cart"):
            pid = product_options[selected]
            msg = controller.add_to_cart(user_id, pid)
            st.success(msg)

    cart_items = controller.cart.get(user_id, [])
    if cart_items:
        for pid in cart_items:
            p = controller.product_agent.get_product_by_id(pid)
            st.markdown(f"🛒 {p['Brand']} - ₹{p['Price']}")
        if st.button("Checkout"):
            msg = controller.purchase_cart(user_id)
            st.success(msg)
    else:
        st.info("Your cart is empty.")
