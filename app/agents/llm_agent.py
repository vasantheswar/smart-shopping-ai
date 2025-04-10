import json
import re

try:
    import ollama
    ollama_available = True
except ImportError:
    ollama_available = False


class LLMQueryAgent:
    def __init__(self, model="phi"):
        if not ollama_available:
            raise RuntimeError("Ollama is not available. Please install it and try again.")
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

            json_match = re.search(r'\{.*?\}', raw, re.DOTALL)
            if not json_match:
                # Return full raw response as AI output
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
        """
        Given a parsed intent JSON and a product agent, return filtered products.
        """
        category = intent.get("category")
        subcategory = intent.get("subcategory")
        max_price = intent.get("max_price")
        tone = intent.get("tone")
        purpose = intent.get("purpose")

        # Step 1: Try subcategory
        if subcategory:
            products = product_agent.get_products_by_subcategory(subcategory, limit=limit)
            if not products:
                subcategory = None
        else:
            products = []

        # Step 2: Fallback to category
        if not products and category:
            products = product_agent.get_products_by_category(category, limit=limit)
            if not products:
                category = None

        # Step 3: Fallback to random
        if not products:
            products = product_agent.get_random_products(limit)

        # Step 4: Filter by price
        if max_price:
            try:
                max_price = float(str(max_price).replace("₹", "").strip())
                filtered = [p for p in products if float(p.get("Price", 0)) <= max_price]
                if filtered:
                    products = filtered
            except:
                pass

        # Step 5: Optional personalization logic
        products = sorted(products, key=lambda x: float(x.get("Price", 0)))

        if tone == "fun":
            products = sorted(products, key=lambda x: "toys" in x.get("Category", "").lower() or "games" in x.get("Subcategory", "").lower(), reverse=True)

        if purpose == "gift":
            products = sorted(products, key=lambda x: "gift" in x.get("Subcategory", "").lower() or "bundle" in x.get("Brand", "").lower(), reverse=True)

        return products
