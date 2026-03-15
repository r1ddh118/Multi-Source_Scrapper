# Multi-Source_Scrapper
This project implements a data scraping pipeline for:
- **3 blog posts**
- **2 YouTube videos**
- **1 PubMed article**

It outputs structured JSON objects with metadata, topic tags, chunked content, and a normalized trust score (`0.0` to `1.0`).

## Project Structure

```text
project/
  scraper/
    blog_scraper.py
    youtube_scraper.py
    pubmed_scraper.py
  scoring/
    trust_score.py
  utils/
    tagging.py
    chunking.py
    regions.py
  output/
    blogs.json
    youtube.json
    pubmed.json
    scraped_data.json
  main.py
  REPORT.md
```

## Required JSON Schema

Each source is stored as:

```json
{
  "source_url": "",
  "source_type": "",
  "author": "",
  "published_date": "",
  "language": "",
  "region": "",
  "topic_tags": [],
  "trust_score": 0.0,
  "content_chunks": []
}
```

## Tools/Libraries Used

- `requests` + `beautifulsoup4` for web extraction
- `youtube-transcript-api` for transcript extraction
- `langdetect` for language detection
- `rake-nltk` (with safe fallback) for topic tagging

## How Scraping Works

### Blogs
- Extracts author, publish date, title, description, and article paragraphs.
- Filters very short `<p>` elements to reduce noise.

### YouTube
- Extracts channel name and publish date from page metadata.
- Pulls transcript when available.
- Uses video description as fallback content context for tags/language.

### PubMed
- Extracts authors, citation/publish text, title, abstract.
- Extracts year for recency scoring.

## Topic Tagging

- Primary: RAKE keyword extraction.
- Fallback: word-frequency-based keyword extraction with stopword filtering.

## Trust Score Design

Implemented in `scoring/trust_score.py`:

```text
Trust Score = f(author_credibility, citation_count, domain_authority, recency, medical_disclaimer_presence)
```

### Weights
- Author credibility: **0.25**
- Citation count: **0.20**
- Domain authority: **0.20**
- Recency: **0.20**
- Medical disclaimer presence: **0.15**

### Score Range
- Clamped to **[0, 1]** and rounded to 3 decimals.

## Edge Cases Handled

- Missing author → reduced author score.
- Missing publish date → fallback recency score.
- Transcript unavailable → placeholder chunk + still process description.
- Multiple authors (PubMed) → author score scales with author list size (capped).
- Non-English content → auto language detection.
- Long articles/transcripts → chunking by segment count and char budget.

## Abuse Prevention Logic

- Low-authority domain + missing author triggers a hard score cap.
- SEO spam-like pages are penalized through domain and author features.
- Missing medical disclaimers reduce score for health content.
- Old publications receive recency penalties.

## Run

```bash
python main.py
```

Generated files are saved under `output/`.

## Limitations

- Some websites may block bots or alter page HTML.
- YouTube transcripts may be unavailable/disabled.
- Domain authority uses rule-based heuristics (not live SEO APIs).