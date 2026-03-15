# trust_score.py

from datetime import datetime

def calculate_trust(author_score, citations, domain_score, publish_year, has_disclaimer):
    current_year = datetime.now().year
    
    recency = max(0, 1 - (current_year - publish_year) / 10)
    
    disclaimer_score = 1 if has_disclaimer else 0
    
    trust = (
        0.25 * author_score + 
        0.25 * citations +
        0.20 * domain_score +
        0.20 * recency + 
        0.15 * disclaimer_score
    )
    
    return round(min(trust, 1), 2)