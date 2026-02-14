import feedparser
import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Mimic a real browser to avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Evergreen Facts for the top card
marketing_facts = [
    "Video content is 50x more likely to drive organic search results than plain text.",
    "70% of marketers are actively investing in content marketing.",
    "Email marketing has an average ROI of $36 for every $1 spent.",
    "93% of online experiences begin with a search engine.",
    "Consistent brand presentation increases revenue by 33%."
]

def get_summary(url):
    """Visits the article to extract the real summary/description."""
    try:
        # 3-second timeout to keep the script fast
        response = requests.get(url, headers=HEADERS, timeout=3)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find the description in standard meta tags
            meta = soup.find('meta', attrs={'name': 'description'}) or \
                   soup.find('meta', attrs={'property': 'og:description'}) or \
                   soup.find('meta', attrs={'name': 'twitter:description'})
            
            if meta and meta.get('content'):
                return meta.get('content').strip()
    except:
        pass
    return "Click to read the full analysis on the source website."

def fetch_content(topic, limit=2):
    print(f"Fetching intel on: {topic}...")
    rss_url = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    
    articles = []
    for entry in feed.entries[:limit]:
        # Fetch the deep summary
        summary_text = get_summary(entry.link)
        
        articles.append({
            "title": entry.title.split(" - ")[0], # Remove source from title
            "source": entry.source.title,
            "link": entry.link,
            "summary": summary_text,
            "type": "NEWS"
        })
        time.sleep(1) # Be polite to servers
    return articles

def main():
    # 1. Daily Fact Card
    daily_fact = {
        "title": random.choice(marketing_facts),
        "source": "Daily Insight",
        "summary": "Key Stat for Digital Marketers",
        "type": "FACT"
    }
    
    # 2. Fetch Deep Intel
    # We fetch fewer articles (2 per topic) but get better quality data
    news_digital = fetch_content("Digital Marketing Trends India")
    news_brand = fetch_content("Brand Strategy Case Study")
    
    # 3. Combine
    feed_data = [daily_fact] + news_digital + news_brand
    
    # 4. Save
    with open('news.json', 'w') as f:
        json.dump(feed_data, f, indent=4)
    print("Intel Feed Updated Successfully.")

if __name__ == "__main__":
    main()
