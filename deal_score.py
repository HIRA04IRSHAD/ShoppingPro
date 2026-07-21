# deal_score.py
def calculate_deal_score(product):
    try:
        # Simple Logic: Discount + Rating influence
        discount = product.get('discount', 0)
        rating = product.get('rating', 0)
        
        # Formula: (Discount * 0.6) + (Rating * 8)
        # Example: 20% off and 4.5 rating -> 12 + 36 = 48
        score = (discount * 0.6) + (rating * 8)
        
        # Sentiment bonus
        if product.get('sentiment') == 'very positive':
            score += 10
        elif product.get('sentiment') == 'positive':
            score += 5
            
        return round(min(score, 100), 2)
    except:
        return 50 # Default score if something fails