# trust_score.py

from datetime import datetime
from urllib.parse import urlparse

def get_domain_score(url):
    domain = urlparse(url).netloc.lower()
    high_trust = ["pubmed", "nih.gov", "who.int", "nature.com"]
    medium_trust = ["youtube.com", "wikipedia.org"]
    if any(d in domain for d in high_trust):
        return 1.0
    elif any(d in domain for d in medium_trust):
        return 0.7
    else:
        return 0.3
    
def get_author_score(author, source_type):
    if not author or author == "Unknown":
        return 0.3
    elif source_type == "pubmed":
        return 0.9
    elif source_type == "youtube":
        return 0.7
    elif source_type == "blog":
        return 0.5
    return 0.4

def get_citation_score(soup):
    links = soup.find_all("a")
    count = len(links)
    return min(count / 50, 1)

def get_recency_score(publish_year):
    if not publish_year:
        return 0.4
    current_year = datetime.now().year
    age = current_year - publish_year
    if age > 10:
        return 0.1
    return max(0, 1 - age / 10)


def has_medical_disclaimer(text):
    keywords = [
        "not medical advice",
        "consult your doctor",
        "for educational purposes",
        "seek professional"
    ]
    text = text.lower()
    return any(k in text for k in keywords)

def calculate_trust(url, author, source_type, publish_year, soup, text):
    domain_score = get_domain_score(url)
    author_score = get_author_score(author, source_type)
    citation_score = get_citation_score(soup)
    recency_score = get_recency_score(publish_year)
    disclaimer_score = 1 if has_medical_disclaimer(text) else 0
    trust = (
        0.25 * author_score +
        0.20 * citation_score +
        0.20 * domain_score +
        0.20 * recency_score +
        0.15 * disclaimer_score
    )
    return round(min(trust, 1), 2)