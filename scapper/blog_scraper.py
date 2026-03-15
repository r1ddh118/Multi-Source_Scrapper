# blog_scaper.py

import requests
from bs4 import BeautifulSoup
from langdetect import detect

def scrape_blog(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    if soup.title:
        title = soup.title.string    
    else:
        title = ""
        
    author = ""
    
    if soup.find("meta", {"name":"author"}):
        author = soup.find("meta", {"name":"author"})["content"]
        
    date = ""
    
    if soup.find("time"):
        data = soup.find("time").text
        
    paragraphs = [p.text for p in soup.find_all("p")]
    content = " ".join(paragraphs)
    
    language = detect(content) if content else "unknown"
    
    return {
        "source_url": url,
        "source_type": "blog",
        "author": author,
        "published_date":date,
        "language": language,
        "region": "",
        "topic_tags": [],
        "trust_score" : "",
        "content_chunks": paragraphs
    }