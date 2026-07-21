from flask import Flask, request, jsonify, render_template
import os
import json
from db_manager import db
from recommender import recommend_products
from deal_score import calculate_deal_score

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '').lower()
        all_products = db.get_all_products()

        # 1. Identity / About ShopAI
        identity_keywords = ["what is shopai", "who are you", "what are you", "about you", "who created you"]
        if any(k in query for k in identity_keywords):
            return jsonify({
                "status": "success",
                "reply": "I am ShopAI, an AI-Powered Smart Shopping Agent! My job is to help you find the best products, score the greatest deals, and stay within your budget. Just tell me what you're looking for (e.g., 'best gaming laptop under 80000').",
                "products": [],
                "type": "info"
            })

        # 2. Customer Support
        support_keywords = ["customer support", "contact support", "help desk", "talk to human", "support", "contact"]
        if any(k in query for k in support_keywords):
            return jsonify({
                "status": "success",
                "reply": "If you need human assistance regarding an order or technical issue, our customer support team is here to help! You can email us at support@shopai.com or call 1800-SHOP-AI. In the meantime, let me know if I can help you find any products!",
                "products": [],
                "type": "info"
            })

        # 3. Handle Landing Page & Category Inquiries
        category_keywords = ["category", "categories", "what do you have", "show categories", "items"]
        if any(k in query for k in category_keywords):
            unique_cats = sorted(list(set(p['category'].capitalize() for p in all_products)))
            cat_list = ", ".join(unique_cats)
            
            # Landing par top 8 products bhej rahe hain
            all_products.sort(key=lambda x: x.get('deal_score', 0), reverse=True)
            landing_products = all_products[:8]
            
            return jsonify({
                "status": "success",
                "reply": f"Welcome to ShopAI! Here are our available categories: {cat_list}. Check out some top picks below!",
                "products": landing_products,
                "type": "info"
            })

        # 4. Search Logic
        results = recommend_products(all_products, query)
        
        if not results:
            return jsonify({
                "status": "success",
                "reply": "I'm sorry, but no items match your search. Please try another keyword!",
                "products": [],
                "type": "empty"
            })

        # 5. Handle Successful Search
        return jsonify({
            "status": "success",
            "reply": f"I found {len(results)} matches for you. Sorting them by the best deals!",
            "products": results,
            "type": "search"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)