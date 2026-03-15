# youtube_scraper.py

from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
from langdetect import detect

def scrape_youtube(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")
    
    channel_tag = soup.find("link", itemprop = "name")
    channel_name = channel_tag["content"] if channel_tag else "Unknown"

    date_tag = soup.find("meta", itemprop="datePublished")
    published_date = date_tag["content"] if date_tag else "Unknown"
    
    desc_tag = soup.find("meta", {"name":"description"})
    description = desc_tag["content"] if desc_tag else ""
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        chunks = [t["text"] for t in transcript]
        full_text = " ".join(chunks)
    except:
        chunks = [description]
        full_text = description
        
    try:
        language = detect(full_text)
    except:
        language = "unknown"
    

    return {
        "source_url": url,
        "source_type": "youtube",
        "author": channel_name,
        "published_date": published_date,
        "language": language,
        "region": "",
        "topic_tags": [],
        "trust_score": "",
        "content_chunks": chunks
    }