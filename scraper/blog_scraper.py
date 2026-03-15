# blog_scaper.py

from __future__ import annotations
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException

from utils.tagging import extract_tags
from utils.chunking import chunk_text
from scoring.trust_score import calculate_trust
from utils.regions import get_region

def _parse_publish_date(soup: BeautifulSoup) -> tuple[str, int | None]:
    candidates = [
        soup.find("meta", {"property": "article:published_time"}),
        soup.find("meta", {"name": "publish_date"}),
        soup.find("meta", {"name": "date"}),
        soup.find("time"),
    ]

    for tag in candidates:
        if not tag:
            continue
        value = tag.get("content") or tag.get_text(strip=True)
        if not value:
            continue

        year_match = re.search(r"\b(19|20)\d{2}\b", value)
        year = int(year_match.group()) if year_match else None
        return value, year

def scrape_blog(url: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")


    author_meta = soup.find("meta", {"name": "author"}) or soup.find("meta", {"property": "author"})
    author = (author_meta.get("content") if author_meta else "") or "Unknown"

    published_date, publish_year = _parse_publish_date(soup)

    title = ""
    og_title = soup.find("meta", {"property": "og:title"})
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    elif soup.title:
        title = soup.title.get_text(strip=True)

    description = ""
    desc_tag = soup.find("meta", {"name": "description"})
    if desc_tag and desc_tag.get("content"):
        description = desc_tag["content"].strip()

    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    paragraphs = [p for p in paragraphs if len(p) > 40]

    full_text = "\n".join([title, description, *paragraphs]).strip()

    try:
        language = detect(full_text) if full_text else "unknown"
    except LangDetectException:
        language = "unknown"

    topic_tags = extract_tags(full_text)
    content_chunks = chunk_text(paragraphs)
    
    trust_score = calculate_trust(
        url=url,
        author=author,
        source_type="blog",
        publish_year=publish_year,
        soup=soup,
        text=full_text,
    )

    region = get_region(url)
    
    return {
        "source_url": url,
        "source_type": "blog",
        "author": author,
        "published_date": published_date,
        "language": language,
        "region": region,
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": content_chunks,
    }