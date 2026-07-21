import json
import os

class DBManager:
    """
    Data Access Layer (DAL) for ShopAI.
    Handles all interactions with the products database.
    """
    def __init__(self, db_path='products.json'):
        self.db_path = db_path
        self.products = self._load_db()

    def _load_db(self):
        """Loads data from the JSON file."""
        if not os.path.exists(self.db_path):
            print(f"Warning: {self.db_path} not found. Creating empty database.")
            return []
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading database: {e}")
            return []

    def get_all_products(self):
        """Returns the full list of products."""
        return self.products

    def get_products_by_category(self, category):
        """Filters products by category (e.g., 'phone', 'laptop')."""
        return [p for p in self.products if p.get('category', '').lower() == category.lower()]

    def get_product_by_id(self, product_id):
        """Fetches a single product by its unique ID."""
        for p in self.products:
            if p.get('id') == product_id:
                return p
        return None

    def search_by_brand(self, brand_name):
        """Filters products by brand."""
        return [p for p in self.products if brand_name.lower() in p.get('brand', '').lower()]

    def save_changes(self):
        """Saves the current state of products back to the JSON file."""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False

# Create a global instance to be used across the app
db = DBManager()