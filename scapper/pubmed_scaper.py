# pubmed_scraper.py

import requests
from bs4 import BeautifulSoup
from langdetect import detect
import re

def scrape_pubmed(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    author = ", ".join([a.text for a in soup.find_all("a", {"class": "full-name"})])
    
    published_date = ""
    publish_year = None

    citation = soup.find("span", {"class": "cit"})
    if citation:
        citation_text = citation.text.strip()

        # Extract full date string (e.g., "2021 Mar 15")
        date_match = re.search(r"(19|20)\d{2}.*?\.", citation_text)
        if date_match:
            published_date = date_match.group().replace(".", "")

        # Extract year only
        year_match = re.search(r"\b(19|20)\d{2}\b", citation_text)
        if year_match:
            publish_year = int(year_match.group())
            
    try:
        language = detect(abstract) if abstract else "unknown"
    except:
        language = "unknown"
        
    abstract_tag = soup.find("div", {"class": "abstract-content"})
    abstract = abstract_tag.text.strip() if abstract_tag else ""
    paragraphs = [abstract]
    
    return {
        "source_url": url,
        "source_type": "pubmed",
        "author": author,
        "published_date": published_date,
        "language": "unknown",
        "region": "",
        "topic_tags": [],
        "trust_score": "",
        "content_chunks": [abstract]
    }
