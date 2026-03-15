# pubmed_scraper.py

from __future__ import annotations
import re

import requests
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException

from utils.tagging import extract_tags
from utils.chunking import chunk_text
from scoring.trust_score import calculate_trust
from utils.regions import get_region

def scrape_pubmed(url: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    author_names = [a.get_text(strip=True) for a in soup.find_all("a", {"class": "full-name"})]
    author = ", ".join(author_names) if author_names else "Unknown"

    citation_text = ""
    citation_tag = soup.find("span", {"class": "cit"})
    if citation_tag:
        citation_text = citation_tag.get_text(" ", strip=True)

    year_match = re.search(r"\b(19|20)\d{2}\b", citation_text)
    publish_year = int(year_match.group()) if year_match else None
    published_date = citation_text or "Unknown"

    abstract_sections = soup.find_all("div", {"class": "abstract-content"})
    abstract_parts = [section.get_text(" ", strip=True) for section in abstract_sections]
    abstract = "\n".join([a for a in abstract_parts if a]).strip()

    title_tag = soup.find("h1", {"class": "heading-title"})
    title = title_tag.get_text(" ", strip=True) if title_tag else ""

    full_text = "\n".join([title, abstract]).strip()
    
    try:
        language = detect(full_text) if full_text else "unknown"
    except LangDetectException:
        language = "unknown"
        
    topic_tags = extract_tags(full_text)
    paragraphs = [p for p in [title, abstract] if p]
    content_chunks = chunk_text(paragraphs, size=1)

    citation_count = len(soup.find_all("a", {"class": "reference-link"}))
    
    region = get_region(url)

    trust_score = calculate_trust(
        url=url,
        author=author,
        source_type="pubmed",
        publish_year=publish_year,
        soup=soup,
        text=full_text,
        citation_count=citation_count,
    )

    return {
        "source_url": url,
        "source_type": "pubmed",
        "author": author,
        "published_date": published_date,
        "language": language,
        "region": region,
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": content_chunks,
    }
