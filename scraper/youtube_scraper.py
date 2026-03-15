# youtube_scraper.py

from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
from langdetect import detect

from utils.tagging import extract_tags
from utils.chunking import chunk_text
from scoring.trust_score import calculate_trust
from utils.regions import get_region

def scrape_youtube(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")
    
    channel_tag = soup.find("link", itemprop = "name")
    channel_name = channel_tag["content"] if channel_tag else "Unknown"

    date_tag = soup.find("meta", itemprop="datePublished")
    published_date = date_tag["content"] if date_tag else "Unknown"
    
    publish_year = None
    if published_date != "Unknown":
        try:
            publish_year = int(published_date[:4])
        except:
            pass
        
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        paragraphs = [t["text"] for t in transcript]
    except:
        paragraphs = ["Transcript unavailable"]

    full_text = " ".join(paragraphs)

        
    try:
        language = detect(full_text) if full_text else "unknown"
    except:
        language = "unknown"
    
    topic_tags = extract_tags(full_text)
    
    content_chunks = chunk_text(paragraphs)
    
    region = get_region(url)

    trust_score = calculate_trust(url=url, author=channel_name, source_type="youtube", publish_year=publish_year, soup=soup, text=full_text)

    return {
        "source_url": url,
        "source_type": "youtube",
        "author": channel_name,
        "published_date": published_date,
        "publication_year": publish_year,
        "language": language,
        "region": region,
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": content_chunks
    }