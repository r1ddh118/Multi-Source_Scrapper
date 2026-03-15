import json

from scraper.youtube_scraper import scrape_youtube
from scraper.blog_scraper import scrape_blog
from scraper.pubmed_scraper import scrape_pubmed

def main():
    all_data = []

    youtube_ids = ["XlMZ46NuEwk", "scDmziIwUEY", "1sISguPDlhY"]
    
    for vid in youtube_ids:
        print(f"Scraping YouTube video: {vid}")
        video_data = scrape_youtube(vid)
        all_data.append(video_data)

    blog_urls = ["https://gi-doctor.medium.com/5-super-reasons-why-you-should-care-for-your-gut-bf812fcf70ba", "https://medium.com/@manas_inquest/the-art-of-a-healthy-gut-d880bcd3f319"]
    for url in blog_urls:
        print(f"Scraping blog post: {url}")
        blog_data = scrape_blog(url)
        all_data.append(blog_data)

    pubmed_urls = ["https://pubmed.ncbi.nlm.nih.gov/41485166/"]
    for url in pubmed_urls:
        print(f"Scraping PubMed article: {url}")
        pubmed_data = scrape_pubmed(url)
        all_data.append(pubmed_data)

    # Save all scraped data to a JSON file
    with open("output/scraped_data.json", "w") as f:
        json.dump(all_data, f, indent=4)
