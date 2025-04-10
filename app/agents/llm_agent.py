import json
import re

# Toggle this to False when deploying to Streamlit Cloud
USE_OLLAMA = False

try:
    if USE_OLLAMA:
        import ollama
        ollama_available = True
    else:
        ollama_available = False
except ImportError:
    ollama_available = False


class LLMQueryAgent:
    def __init__(self, model="phi"):
        if not ollama_available:
            raise RuntimeError("LLM agent is not available in this environment.")
        self.model = model

    def ask(self, prompt, max_tokens=200):
        system_prompt = (
            "You are a smart shopping assistant. Return the user's shopping intent as a JSON object and optionally provide a short explanation or text output if necessary.\n"
            "Use these keys: category, subcategory, max_price, purpose, tone.\n"
            "If any field is not mentioned, set it to null.\n\n"
            "Example input: Suggest a gift under ₹500 for a teenager\n"
            "Example output:\n"
            "{\n"
            "  \"category\": null,\n"
            "  \"subcategory\": \"gadgets\",\n"
            "  \"max_price\": 500,\n"
            "  \"purpose\": \"gift\",\n"
            "  \"tone\": \"fun\"\n"
            "}\n\n"
            f"User: {prompt}\n"
            "Output:"
        )

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": system_prompt}]
            )
            raw = response['message']['content']

            # Try to extract JSON
            json_match = re.search(r'\{.*?\}', raw, re.DOTALL)
            if not json_match:
                return {
                    "category": None,
                    "subcategory": None,
                    "max_price": None,
                    "purpose": None,
                    "tone": None,
                    "ai_output": raw.strip(),
                    "error": "No structured JSON found. Showing raw AI response."
                }

            json_data = json_match.group(0)
            parsed = json.loads(json_data)
            return parsed

        except Exception as e:
            return {
                "category": None,
                "subcategory": None,
                "max_price": None,
                "purpose": None,
                "tone": None,
                "error": f"Failed to parse LLM output: {e}",
                "raw_response": raw if 'raw' in locals() else "No response"
            }

    def filter_products_from_intent(self, intent, product_agent, limit=10):
        category = intent.get("category")
        subcategory = intent.get("subcategory")
        max_price = intent.get("max_price")
        tone = intent.get("tone")
        purpose = intent.get("purpose")

        # Step 1: Try subcategory
        products = []
        if subcategory:
            products = product_agent.get_products_by_subcategory(subcategory, limit=limit)
            if not products:
                subcategory = None

        # Step 2: Try category
        if not products and category:
            products = product_agent.get_products_by_category(category, limit=limit)
            if not products:
                category = None

        # Step 3: Random fallback
        if not products:
            products = product_agent.get_random_products(limit)

        # Step 4: Filter by max price
        if max_price:
            try:
                max_price = float(str(max_price).replace("₹", "").strip())
                products = [p for p in products if float(p.get("Price", 0)) <= max_price]
            except:
                pass

        # Step 5: Personalize by tone/purpose
        products = sorted(products, key=lambda x: float(x.get("Price", 0)))
        if tone == "fun":
            products = sorted(products, key=lambda x: "toy" in x.get("Category", "").lower() or "game" in x.get("Subcategory", "").lower(), reverse=True)
        if purpose == "gift":
            products = sorted(products, key=lambda x: "gift" in x.get("Subcategory", "").lower() or "bundle" in x.get("Brand", "").lower(), reverse=True)

        return products
