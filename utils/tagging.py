# tagging.py

import re
from collections import Counter
from typing import List

try:
    from rake_nltk import Rake
except Exception:  # pragma: no cover - fallback path
    Rake = None

STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "from", "your", "have", "has",
    "are", "was", "were", "will", "would", "can", "could", "about", "into", "their",
    "them", "they", "you", "our", "not", "but", "what", "when", "where", "which",
}


def _fallback_tags(text: str, top_n: int) -> List[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", text.lower())
    words = [w for w in words if w not in STOPWORDS]
    return [w for w, _ in Counter(words).most_common(top_n)]


def extract_tags(text: str, top_n: int = 6) -> List[str]:
    if not text or not text.strip():
        return []

    if Rake is None:
        return _fallback_tags(text, top_n)

    try:
        rake = Rake()
        rake.extract_keywords_from_text(text)
        phrases = [p.strip() for p in rake.get_ranked_phrases() if p.strip()]
        if phrases:
            return phrases[:top_n]
    except Exception:
        pass

    return _fallback_tags(text, top_n)
