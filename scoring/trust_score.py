# trust_score.py

from __future__ import annotations
from datetime import datetime
from urllib.parse import urlparse
from typing import Optional

def get_domain_score(url: str) -> float:
    domain = urlparse(url).netloc.lower()
    high_trust = ["pubmed", "nih.gov", "who.int", "nature.com", "thelancet.com", "nejm.org"]
    medium_trust = ["youtube.com", "medium.com", "substack.com"]

    if any(d in domain for d in high_trust):
         return 0.95
    if any(d in domain for d in medium_trust):
        return 0.70
    return 0.35


def get_author_score(author: str, source_type: str) -> float:
    if not author or author.strip().lower() in {"unknown", ""}:
        return 0.25

    if source_type == "pubmed":
        author_count = max(1, len([a for a in author.split(",") if a.strip()]))
        return min(0.75 + 0.03 * author_count, 0.92)

    if source_type == "youtube":
        return 0.62

    if source_type == "blog":
        return 0.50

    return 0.40


def get_citation_score(citation_count: Optional[int], soup) -> float:
    if citation_count is None:
        citation_count = len(soup.find_all("a")) if soup else 0
    return min(citation_count / 20.0, 1.0)


def get_recency_score(publish_year: Optional[int]) -> float:
    if not publish_year:
        return 0.35
    current_year = datetime.now().year
    age = current_year - publish_year
    if age <= 1:
        return 1.0
    if age >= 12:
        return 0.1
    return max(0.1, 1 - (age / 12))


def has_medical_disclaimer(text: str) -> bool:
    text = (text or "").lower()
    keywords = [
        "not medical advice",
        "consult your doctor",
        "for educational purposes",
        "seek professional"
    ]
    return any(k in text for k in keywords)

def calculate_trust(
    url: str,
    author: str,
    source_type: str,
    publish_year: Optional[int],
    soup=None,
    text: str = "",
    citation_count: Optional[int] = None,
) -> float:
    author_score = get_author_score(author, source_type)
    citation_score = get_citation_score(citation_count, soup)
    domain_score = get_domain_score(url)
    recency_score = get_recency_score(publish_year)
    disclaimer_score = 1.0 if has_medical_disclaimer(text) else 0.0
    trust = (
        0.25 * author_score
        + 0.20 * citation_score
        + 0.20 * domain_score
        + 0.20 * recency_score
        + 0.15 * disclaimer_score
    )
    if domain_score < 0.5 and author_score <= 0.25:
        trust = min(trust, 0.45)

    return round(max(0.0, min(trust, 1.0)), 3)
