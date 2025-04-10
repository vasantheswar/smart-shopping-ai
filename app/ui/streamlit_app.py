import sys
import os
import sqlite3

# Add the project root (smart_shopping_agent/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
from app.main import AgentController
from app.agents.llm_agent import LLMQueryAgent

# ---------- Page Styling ---------- #
st.set_page_config(page_title="Smart Shopping AI", layout="wide")
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-size: 1.1rem;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    h2 { font-size: 28px !important; }
    h3 { font-size: 24px !important; }

    .section-header { margin-top: 3rem; margin-bottom: 1.5rem; font-size: 24px; font-weight: 600; }

    .product-card {
        background: linear-gradient(to bottom right, #e0f2fe, #ffffff);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 1.5rem;
        font-size: 18px;
    }

    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
        gap: 2rem;
        margin-top: 1.5rem;
    }

    code {
        font-size: 1.1rem;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        background-color: #1e293b;
        color: #22c55e;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Initialize Controller ---------- #
st.title("Smart Shopping - Personalized E-Commerce AI")
controller = AgentController()

# ---------- Sidebar Controls ---------- #
st.sidebar.header("User Settings")
try:
    conn = sqlite3.connect("app/database/smartshop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Customer_ID FROM customer_data_collection LIMIT 100")
    rows = cursor.fetchall()
    available_users = [row[0] for row in rows]
    user_map = {str(row[0]): str(row[0]) for row in rows}
    conn.close()
except:
    available_users = ["C1001"]
    user_map = {"C1001": "C1001"}

selected_user = st.sidebar.selectbox("Select User", available_users)
user_id = user_map[selected_user]  # Ensure user_id is like 'C1001'

search_type = st.sidebar.selectbox("Search By", ["Category", "Subcategory"])
query = st.sidebar.text_input("Enter search term")

# ---------- Tabs ---------- #
dashboard_tab, cart_tab, assistant_tab = st.tabs(["Dashboard", "Cart", "AI Assistant"])

# ---------- Dashboard Tab ---------- #
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

        st.markdown("<div class='section-header'>Recommended Products</div>", unsafe_allow_html=True)
        st.markdown("<div class='product-grid'>", unsafe_allow_html=True)
        for rec in dashboard["recommendations"]:
            st.markdown(f"""
                <div class='product-card'>
                    <strong>{rec.get('Brand', 'Product')}</strong> - ₹{rec.get('Price', 'N/A')}<br>
                    Category: <code>{rec.get('Category', '')}</code><br>
                    Subcategory: <code>{rec.get('Subcategory', '')}</code>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if query:
            st.markdown(f"<div class='section-header'>Search Results for '{query}' ({search_type})</div>", unsafe_allow_html=True)
            results = (controller.search_products_by_category(query)
                       if search_type == "Category"
                       else controller.search_products_by_tag(query))
            if results:
                st.markdown("<div class='product-grid'>", unsafe_allow_html=True)
                for product in results:
                    st.markdown(f"""
                        <div class='product-card'>
                            <strong>{product.get('Brand')}</strong> - ₹{product.get('Price')}<br>
                            Category: <code>{product.get('Category')}</code><br>
                            Subcategory: <code>{product.get('Subcategory')}</code>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No matching products found.")

# ---------- Cart Tab ---------- #
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
            st.markdown(f"🧾 {p['Brand']} - ₹{p['Price']}")
        if st.button("Checkout"):
            msg = controller.purchase_cart(user_id)
            st.success(msg)
    else:
        st.info("Cart is currently empty.")

# ---------- AI Assistant Tab ---------- #
with assistant_tab:
    st.subheader("Smart Shopping Assistant")
    try:
        llm_agent = LLMQueryAgent(model="phi")
        user_query = st.text_input("Ask a shopping question like 'suggest gifts under ₹1000'")

        if st.button("Ask Assistant"):
            with st.spinner("Thinking..."):
                result = llm_agent.ask(user_query)

            if "error" in result:
                st.warning(f"Error: {result['error']}")
                st.code(result.get("raw_response", ""))
            else:
                st.markdown("**Interpreted Intent**")
                st.json(result)

                products = llm_agent.filter_products_from_intent(result, controller.product_agent, limit=10)
                if products:
                    st.markdown("<div class='section-header'>Recommended by AI</div>", unsafe_allow_html=True)
                    st.markdown("<div class='product-grid'>", unsafe_allow_html=True)
                    for p in products:
                        st.markdown(f"""
                            <div class='product-card'>
                                <strong>{p['Brand']}</strong> - ₹{p['Price']}<br>
                                Category: <code>{p['Category']}</code><br>
                                Subcategory: <code>{p['Subcategory']}</code>
                            </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("No recommendations matched your query.")
    except Exception as e:
        st.error(f"Failed to load AI assistant: {e}")