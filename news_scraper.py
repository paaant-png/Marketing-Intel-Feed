import feedparser
import json
import random
from datetime import datetime

# --- PART 1: THE BACKUP DATABASE (Guaranteed Content) ---
# If Google blocks us, show these instead of an empty screen.
backup_news = [
    {"title": "The Ultimate Guide to SEO in 2026", "source": "Search Engine Land", "link": "https://searchengineland.com", "type": "NEWS"},
    {"title": "How AI is Reshaping Digital Marketing", "source": "HubSpot Blog", "link": "https://blog.hubspot.com/marketing", "type": "NEWS"},
    {"title": "10 Trends in Brand Strategy for India", "source": "Campaign India", "link": "https://www.campaignindia.in", "type": "NEWS"},
    {"title": "Why Video Content dominates Social Media", "source": "Social Media Today", "link": "https://www.socialmediatoday.com", "type": "NEWS"}
]

marketing_facts = [
    "Did you know? Video content is 50x more likely to drive organic search results than plain text.",
    "Fact: 70% of marketers are actively investing in content marketing.",
    "Insight: Email marketing has an average ROI of $36 for every $1 spent.",
    "Stat: 93% of online experiences begin with a search engine.",
    "Branding: Consistent presentation of a brand has been seen to increase revenue by 33%."
]

def fetch_rss(url, tag):
    print(f"Attempting to fetch {tag}...")
    try:
        # standard feedparser call
        feed = feedparser.parse(url)
        articles = []
        if feed.entries:
            for entry in feed.entries[:3]:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": entry.source.title if hasattr(entry, 'source') else "Google News",
                    "date": "Today",
                    "type": "NEWS"
                })
            print(f"Success: Found {len(articles)} items for {tag}")
            return articles
        else:
            print(f"Warning: No entries found for {tag}")
            return []
    except Exception as e:
        print(f"Error fetching {tag}: {e}")
        return []

def main():
    # 1. Generate Daily Fact
    daily_fact = {
        "title": random.choice(marketing_facts),
        "link": "#",
        "source": "Marketing Insight",
        "date": datetime.now().strftime("%d %b"),
        "type": "FACT"
    }
    
    # 2. Try Fetching Live News (Digital Marketing & Branding)
    # We use a broader search query to ensure results
    news_items = fetch_rss("https://news.google.com/rss/search?q=Digital+Marketing+Trends&hl=en-IN&gl=IN&ceid=IN:en", "Digital Marketing")
    
    # 3. Fail-Safe Logic
    if len(news_items) == 0:
        print("Live fetch failed. Using Backup Database.")
        final_feed = [daily_fact] + backup_news
    else:
        final_feed = [daily_fact] + news_items

    # 4. Save to JSON
    with open('news.json', 'w') as f:
        json.dump(final_feed, f, indent=4)
    print("Job Complete. news.json updated.")

if __name__ == "__main__":
    main()
