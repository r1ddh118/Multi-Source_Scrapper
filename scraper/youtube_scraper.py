# youtube_scraper.py

from __future__ import annotations
import re

from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException

from utils.tagging import extract_tags
from utils.chunking import chunk_text
from scoring.trust_score import calculate_trust
from utils.regions import get_region

def _extract_description(soup: BeautifulSoup) -> str:
    tag = soup.find("meta", {"name": "description"})
    return tag.get("content", "").strip() if tag else ""


def scrape_youtube(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    channel_tag = soup.find("link", itemprop="name")
    channel_name = channel_tag.get("content") if channel_tag else "Unknown"

    date_tag = soup.find("meta", itemprop="datePublished")
    published_date = date_tag.get("content") if date_tag else "Unknown"
    publish_year = None
    
    if published_date and published_date != "Unknown":
        year_match = re.search(r"\b(19|20)\d{2}\b", published_date)
        if year_match:
            publish_year = int(year_match.group())

    description = _extract_description(soup)

    transcript_segments = []
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_segments = [segment.get("text", "").strip() for segment in transcript if segment.get("text")]
    except Exception:
        transcript_segments = []
    base_parts = [description] + transcript_segments
    full_text = "\n".join([p for p in base_parts if p]).strip()

    if not transcript_segments:
        transcript_segments = ["Transcript unavailable"]
        
    try:
        language = detect(full_text) if full_text else "unknown"
    except LangDetectException:
        language = "unknown"
    
    topic_tags = extract_tags(full_text)
    
    content_chunks = chunk_text(transcript_segments)

    region = get_region(url)

    trust_score = calculate_trust(
        url=url,
        author=channel_name,
        source_type="youtube",
        publish_year=publish_year,
        soup=soup,
        text=full_text,
    )

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