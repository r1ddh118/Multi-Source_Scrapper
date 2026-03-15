# Short Report: Scraping Strategy & Trust Scoring

## 1) Scraping Strategy

The pipeline uses source-specific scrapers:

- **Blog scraper** extracts metadata from common tags (`author`, publish-time tags, title/description) and article paragraphs.
- **YouTube scraper** collects channel + date from metadata and attempts transcript extraction via `youtube-transcript-api`.
- **PubMed scraper** collects title, authors, citation string, publication year, and abstract sections.

All data is normalized to one shared schema and saved to JSON files (`blogs.json`, `youtube.json`, `pubmed.json`, plus merged `scraped_data.json`).

## 2) Topic Tagging Method

Topic extraction is performed with:
1. **RAKE** keyword extraction.
2. **Fallback frequency-based tagging** when RAKE/resources fail.

This makes tagging robust in environments where NLTK corpora are partially unavailable.

## 3) Trust Score Algorithm

The scoring function is:

```text
Trust Score = f(author_credibility, citation_count, domain_authority, recency, medical_disclaimer_presence)
```

A weighted sum is used:

- Author credibility (0.25)
- Citation count (0.20)
- Domain authority (0.20)
- Recency (0.20)
- Medical disclaimer presence (0.15)

The final output is clamped to `[0, 1]`.

## 4) Edge Case Handling

- Missing author/date/transcript handled with defaults.
- Multiple authors on PubMed are rewarded with an averaged/scaled credibility score (capped).
- Non-English text is supported by automatic language detection.
- Long content is chunked into bounded blocks for downstream processing.

## 5) Abuse Prevention

- Unknown author + low authority domain triggers a trust cap.
- SEO spam blogs are penalized by domain/author features.
- Outdated content receives stronger recency penalties.
- Missing medical disclaimers reduce confidence in health content.