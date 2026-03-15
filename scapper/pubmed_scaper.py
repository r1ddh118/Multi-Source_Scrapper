# pubmed_scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_pubmed(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    if soup.find("h1"):
        title = soup.find("h1").text
    else:
        title = ""

    author = ", ".join([a.text for a in soup.find_all("a", {"class": "full-name"})])
    
    published_date = soup.find("meta", {"name": "date"})["content"] if soup.find("meta", {"name": "date"}) else ""
    abstract = soup.find("div", {"class": "abstract"}).text if soup.find("div", {"class": "abstract"}) else ""

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
