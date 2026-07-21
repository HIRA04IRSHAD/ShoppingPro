"""
ShopAI - Smart Product Recommender Engine
Optimized for B.Tech Final Submission
"""
import re

# Category mapping to handle synonyms
CATEGORY_MAP = {
    "phone": ["phone", "mobile", "smartphone", "handset", "redmi", "samsung", "realme", "poco", "oneplus", "vivo", "infinix", "nothing", "motorola", "moto", "iphone"],
    "laptop": ["laptop", "notebook", "computer", "pc", "chromebook", "macbook"],
    "headphones": ["headphone", "headset", "over ear", "on ear", "noise cancel"],
    "earphones": ["earphone", "earbuds", "tws", "earbud", "airpods", "buds", "in ear", "neckband"],
    "tv": ["tv", "television", "smart tv", "led", "oled", "screen"],
    "ac": ["ac", "air conditioner", "cooler", "inverter ac", "split ac"],
    "smartwatch": ["smartwatch", "watch", "fitness band", "smart band", "wearable"],
    "accessories": ["accessory", "accessories", "keyboard", "mouse", "hub", "powerbank", "power bank", "charger", "cable"],
    "appliances": ["fridge", "refrigerator", "washing machine", "washer", "microwave", "kettle", "air fryer", "appliance"],
    "tablet": ["tablet", "ipad", "tab", "drawing tablet"]
}

FEATURE_KEYWORDS = [
    "camera", "battery", "gaming", "fast charging", "5g", "wireless",
    "noise cancellation", "bass", "amoled", "lightweight", "coding",
    "performance", "budget", "premium", "4k", "hdr", "energy saving",
    "inverter", "rgb", "tws", "slim", "gps", "waterproof"
]

def detect_category(query):
    query = query.lower()
    matched = []
    for category, synonyms in CATEGORY_MAP.items():
        for syn in synonyms:
            if syn in query:
                if category not in matched:
                    matched.append(category)
    return matched

def extract_budget(query):
    """Robust budget extraction using Regex with above/below detection"""
    query = query.lower().replace(",", "").replace("₹", "").replace("rs", "")
    
    # Detect if user wants "above" a certain price
    is_above = any(word in query for word in ["above", "over", "more than", "greater than"])
    
    # Check for "k" format (e.g., 20k)
    k_match = re.search(r'(\d+)\s*k\b', query)
    budget_val = None
    
    if k_match:
        budget_val = int(k_match.group(1)) * 1000
    else:
        # Extract all numbers and find the one most likely to be a budget
        nums = re.findall(r'\d+', query)
        if nums:
            # Filter: Numbers between 500 and 300,000 are usually budgets
            valid_budgets = [int(n) for n in nums if 500 <= int(n) <= 300000]
            if valid_budgets:
                budget_val = max(valid_budgets)
                
    if budget_val:
        if is_above:
            return {"min": budget_val, "max": float('inf')} # No upper limit
        else:
            return {"min": 0, "max": budget_val} # Standard "under X" query
            
    return {"min": 0, "max": float('inf')} # No budget mentioned


def recommend_products(products, query, budget_range=None):
    # Circular Import Fix: Import inside function
    from deal_score import calculate_deal_score
    
    query = query.lower()
    if not budget_range:
        budget_range = extract_budget(query)

    categories = detect_category(query)
    features = [f for f in FEATURE_KEYWORDS if f in query]

    results = []
    for p in products:
        score = 0
        
        # 1. Category Filtering (Crucial)
        if categories and p["category"] not in categories:
            continue
        if categories: score += 50 # Base score for right category

        # 2. Budget Filtering (Updated for above/below)
        if p["price"] < budget_range["min"] or p["price"] > budget_range["max"]:
            continue
            
        # Value for money boost (only if there is a max budget)
        if budget_range["max"] != float('inf') and p["price"] >= (budget_range["max"] * 0.8):
            score += 20

        # 3. Brand & Feature Matching
        if p["brand"].lower() in query:
            score += 30
        
        matched_features = [f for f in features if f in p.get("features", [])]
        score += len(matched_features) * 15

        # 4. Keyword/Tag Matching
        p_tags = " ".join(p.get("tags", [])).lower()
        for word in query.split():
            if len(word) > 3 and word in p_tags:
                score += 10

        # Calculate Final Stats
        p_copy = dict(p)
        p_copy["deal_score"] = calculate_deal_score(p)
        p_copy["match_score"] = score
        results.append(p_copy)

    # Sort by Match Score first, then Deal Score as tie-breaker
    results.sort(key=lambda x: (x["match_score"], x["deal_score"]), reverse=True)
    return results
def compare_products(products, ids):
    from deal_score import calculate_deal_score
    result = []
    for p in products:
        if str(p["id"]) in [str(i) for i in ids]:
            p_copy = dict(p)
            p_copy["deal_score"] = calculate_deal_score(p)
            result.append(p_copy)
    return result