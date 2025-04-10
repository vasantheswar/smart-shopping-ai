# Smart Shopping AI 🛒

**Smart Shopping Assistant** is a GenAI-powered, agent-based e-commerce solution designed to enhance user experience through personalized recommendations, contextual shopping assistance, and intelligent product discovery.

## 💡 Problem Statement

This project addresses **Problem Statement 2: Smart Shopping – Data and AI for Personalized E-Commerce** from the Accenture GenAI Hackathon. The goal is to simplify online shopping using data-driven personalization and AI-powered decision support.

## 🚀 Features

- 🎯 Personalized product recommendations using user profile and behavior
- 💬 LLM-powered shopping assistant for natural language queries
- 📊 Context-aware filtering (price, category, subcategory, tone)
- 🛍️ Cart simulation and purchase tracking
- 🔍 Semantic search via AI assistant
- 🧠 Built with agent architecture: user agent, product agent, recommender agent, and LLM query agent

## 🧱 Tech Stack

| Layer        | Technologies Used                                      |
|--------------|--------------------------------------------------------|
| **Frontend** | Streamlit (custom UI, responsive layout)               |
| **Backend**  | Python, SQLite, Pandas                                 |
| **AI/LLM**   | [Phi-2](https://huggingface.co/microsoft/phi-2) via Ollama |
| **Infra**    | GitHub, Hugging Face, Local execution (no cloud needed) |

## 🧠 Architecture Overview

User → Streamlit UI → Agent Controller → [UserAgent | ProductAgent | RecommenderAgent | LLMQueryAgent]



All components interact through a central controller which routes the requests based on user interaction and LLM understanding.

## 📂 Project Structure

smart_shopping_agent/ ├── app/ │ ├── agents/ │ │ ├── user_agent.py │ │ ├── product_agent.py │ │ ├── recommender_agent.py │ │ └── llm_agent.py │ ├── database/ │ │ └── smartshop.db │ ├── data/ │ │ ├── customer_data_collection.csv │ │ └── product_recommendation_data.csv │ ├── main.py │ └── ui/ │ └── streamlit_app.py


## 🧪 Demo

- **Web App (Local)**: Run via `streamlit run app/ui/streamlit_app.py`
- **Demo Video**: _[Add your video link here]_

## 📦 How to Run

```bash
git clone https://github.com/YOUR_USERNAME/smart-shopping-ai.git
cd smart-shopping-ai
pip install -r requirements.txt
streamlit run app/ui/streamlit_app.py
💬 Make sure ollama and the phi model are installed locally.

📍 Team Info
Team Name: SMARTSOULS
Contributors:
Ch. VASANTH ESWAR
B. SANDEEP RAGHAVENDRA


📌 Built for Accenture's GenAI Hackathon - 2025