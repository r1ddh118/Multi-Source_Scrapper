# tagging.py

from rake_nltk import Rake

def extract_tags(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()[:5]