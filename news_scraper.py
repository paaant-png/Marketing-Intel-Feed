import feedparser
import json
import random
from datetime import datetime
import re

# --- PART 1: RELIABLE SOURCES (That provide summaries) ---
# We use Bing News and Industry Feeds because they include the 'description' text in the feed itself.
RSS_SOURCES = [
    {
        "tag": "Digital Marketing",
        "url": "https://www.marketingdive.com/feeds/news/",
        "source": "Marketing Dive"
    },
    {
        "tag": "SEO & Trends",
        "url": "https://searchengineland.com/feed",
        "source": "Search Engine Land"
    },
    {
        "tag": "Brand Strategy",
        "url": "https://www.bing.com/news/search?q=Brand+Strategy+India&format=rss",
        "source": "Bing News"
    }
]

# Evergreen Facts for the Sidebar
marketing_facts = [
    "Video content is 50x more likely to drive organic search results than plain text.",
    "70% of marketers are actively investing in content marketing.",
    "Email marketing has an average ROI of $36 for every $1 spent.",
    "93% of online experiences begin with a search engine.",
    "Consistent brand presentation increases revenue by 33%."
]

def clean_html(raw_html):
    """Removes HTML tags (like <p>, <a>) from the summary text."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext[:250] + "..." if len(cleantext) > 250 else cleantext

def fetch_feed(source_config):
    print(f"Fetching from {source_config['source']}...")
    try:
        feed = feedparser.parse(source_config['url'])
        articles = []
        
        # Get top 2 articles from each source
        for entry in feed.entries[:2]:
            # 1. Try to find the summary in different common RSS fields
            raw_summary = ""
            if hasattr(entry, 'summary'):
                raw_summary = entry.summary
            elif hasattr(entry, 'description'):
                raw_summary = entry.description
            
            # 2. Clean it up
            clean_summary = clean_html(raw_summary)
            
            # 3. Fallback if empty
            if len(clean_summary) < 20:
                clean_summary = "Click to read the full market analysis."

            articles.append({
                "title": entry.title,
                "link": entry.link,
                "source": source_config['source'],
                "summary": clean_summary,
                "type": "NEWS"
            })
        return articles
    except Exception as e:
        print(f"Error fetching {source_config['source']}: {e}")
        return []

def main():
    # 1. Sidebar Fact
    daily_fact = {
        "title": random.choice(marketing_facts),
        "source": "Stat of the Day",
        "summary": "Key insight for your strategy.",
        "type": "FACT"
    }
    
    # 2. Fetch All News
    all_news = []
    for source in RSS_SOURCES:
        news_items = fetch_feed(source)
        all_news.extend(news_items)
        
    # 3. Combine (Fact first)
    final_feed = [daily_fact] + all_news
    
    # 4. Save
    with open('news.json', 'w') as f:
        json.dump(final_feed, f, indent=4)
    print(f"Success! Generated {len(final_feed)} unique insights.")

if __name__ == "__main__":
    main()
