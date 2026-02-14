import feedparser
import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# --- CONSTANTS ---
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

marketing_facts = [
    "Did you know? Video content is 50x more likely to drive organic search results than plain text.",
    "Fact: 70% of marketers are actively investing in content marketing.",
    "Insight: Email marketing has an average ROI of $36 for every $1 spent.",
    "Stat: 93% of online experiences begin with a search engine.",
    "Branding: Consistent presentation of a brand has been seen to increase revenue by 33%."
]

def get_meta_summary(url):
    """
    Visits the article URL and extracts the 'Description' meta tag.
    This acts as a perfect 1-sentence summary.
    """
    try:
        # We need a headers dict to look like a real browser, otherwise sites block us
        headers = {'User-Agent': USER_AGENT}
        
        # Timeout is short (3s) so we don't get stuck if a site is slow
        response = requests.get(url, headers=headers, timeout=3, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find standard description or OpenGraph description
            meta = soup.find('meta', attrs={'name': 'description'}) or \
                   soup.find('meta', attrs={'property': 'og:description'}) or \
                   soup.find('meta', attrs={'name': 'twitter:description'})
            
            if meta and meta.get('content'):
                summary = meta.get('content').strip()
                # Keep it short (max 200 chars)
                return summary[:200] + "..." if len(summary) > 200 else summary
                
    except Exception:
        pass # If we fail, just return None
    
    return "Click to read the full story on the publisher's website."

def fetch_rss(url, tag):
    print(f"Fetching {tag}...")
    feed = feedparser.parse(url)
    articles = []
    
    # Limit to top 2 articles per topic to keep the script fast
    for entry in feed.entries[:2]:
        # Fetch the real summary from the website
        print(f"  - Summarizing: {entry.title[:30]}...")
        summary_text = get_meta_summary(entry.link)
        
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "source": entry.source.title if hasattr(entry, 'source') else "News",
            "date": "Today",
            "summary": summary_text,
            "type": "NEWS"
        })
        # Be polite to servers
        time.sleep(1)
        
    return articles

def main():
    # 1. Daily Fact
    daily_fact = {
        "title": random.choice(marketing_facts),
        "link": "#",
        "source": "Marketing Insight",
        "date": datetime.now().strftime("%d %b"),
        "summary": "Daily knowledge bite for smarter marketing.",
        "type": "FACT"
    }
    
    # 2. Fetch News (Using a broader search to ensure hits)
    digital_news = fetch_rss("https://news.google.com/rss/search?q=Digital+Marketing+Trends+India&hl=en-IN&gl=IN&ceid=IN:en", "Digital Marketing")
    brand_news = fetch_rss("https://news.google.com/rss/search?q=Brand+Strategy+Innovation&hl=en-IN&gl=IN&ceid=IN:en", "Branding")
    
    # 3. Combine
    final_feed = [daily_fact] + digital_news + brand_news

    # 4. Save
    with open('news.json', 'w') as f:
        json.dump(final_feed, f, indent=4)
    print("Done. Summaries generated.")

if __name__ == "__main__":
    main()
