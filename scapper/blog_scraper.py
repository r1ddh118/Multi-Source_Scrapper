# blog_scaper.py

import requests
from bs4 import BeautifulSoup
from langdetect import detect

from utils.tagging import extract_tags
from utils.chunking import chunk_text
from scoring.trust_score import calculate_trust

def scrape_blog(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
        
    author = ""
    
    if soup.find("meta", {"name":"author"}):
        author = soup.find("meta", {"name":"author"})["content"]

    published_date = ""

    if soup.find("time"):
        published_date = soup.find("time").text
    
    if published_date:
        try:
            publish_year = int(published_date[-4:])
        except:
            pass

    paragraphs = [p.text for p in soup.find_all("p")]
    full_text = " ".join(paragraphs)

    language = detect(full_text) if full_text else "unknown"

    topic_tags = extract_tags(full_text)
    content_chunks = chunk_text(paragraphs)
    
    trust_score = calculate_trust(url, author, "blog", publish_year, soup, full_text)
    
    return {
        "source_url": url,
        "source_type": "blog",
        "author": author,
        "published_date": published_date,
        "language": language,
        "region": "",
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": content_chunks
    }