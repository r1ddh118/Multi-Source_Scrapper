import json
from pathlib import Path

from scraper.youtube_scraper import scrape_youtube
from scraper.blog_scraper import scrape_blog
from scraper.pubmed_scraper import scrape_pubmed
from scraper.youtube_scraper import scrape_youtube


OUTPUT_DIR = Path("output")


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2, ensure_ascii=False)

def main():
    all_data = []

    youtube_ids = ["XlMZ46NuEwk", "scDmziIwUEY"]
    blog_urls = [
        "https://en.wikipedia.org/wiki/Healthy_digestion",
        "https://en.wikipedia.org/wiki/Gut_Health",
        "https://en.wikipedia.org/wiki/Healthy_diet",
    ]
    pubmed_urls = ["https://pubmed.ncbi.nlm.nih.gov/41485166/"]

    youtube_data = []
    blog_data = []
    pubmed_data = []

    for video_id in youtube_ids:
        print(f"Scraping YouTube video: {video_id}")
        item = scrape_youtube(video_id)
        youtube_data.append(item)
        all_data.append(item)

    for url in blog_urls:
        print(f"Scraping blog post: {url}")
        item = scrape_blog(url)
        blog_data.append(item)
        all_data.append(item)

    pubmed_urls = ["https://pubmed.ncbi.nlm.nih.gov/41485166/"]
    for url in pubmed_urls:
        print(f"Scraping PubMed article: {url}")
        item = scrape_pubmed(url)
        pubmed_data.append(item)
        all_data.append(item)

    _write_json(OUTPUT_DIR / "youtube.json", youtube_data)
    _write_json(OUTPUT_DIR / "blogs.json", blog_data)
    _write_json(OUTPUT_DIR / "pubmed.json", pubmed_data)
    _write_json(OUTPUT_DIR / "scraped_data.json", all_data)

    print(f"Saved {len(all_data)} sources to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
