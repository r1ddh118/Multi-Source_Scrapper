from urllib.parse import urlparse


def get_region(url):

    domain = urlparse(url).netloc.lower()

    if ".in" in domain:
        return "India"

    if ".uk" in domain:
        return "United Kingdom"

    if ".au" in domain:
        return "Australia"

    if ".ca" in domain:
        return "Canada"

    if "youtube.com" in domain:
        return "Global"

    if "pubmed" in domain or "nih.gov" in domain:
        return "United States"

    return "Unknown"