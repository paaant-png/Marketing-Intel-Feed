import feedparser
import json
import random
from datetime import datetime

# --- PART 1: STATIC KNOWLEDGE BASE (Evergreen Facts) ---
marketing_facts = [
    "Did you know? Video content is 50x more likely to drive organic search results than plain text.",
    "Fact: 70% of marketers are actively investing in content marketing.",
    "Insight: Email marketing has an average ROI of $36 for every $1 spent.",
    "Stat: 93% of online experiences begin with a search engine.",
    "Trend: 'Near Me' searches have grown by over 900% in the last two years.",
    "Branding: Consistent presentation of a brand has been seen to increase revenue by 33%.",
    "Social: Visual content is more than 40x more likely to get shared on social media.",
    "SEO: The first 5 results on Google get 67% of all clicks."
]

def fetch_google_news(topic):
    # Google News RSS URL for specific topics in India (ceid=IN:en)
    encoded_topic = topic.replace(" ", "%20")
    rss_url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(rss_url)
    articles = []

    # Get top 3 stories per topic to keep it curated
    for entry in feed.entries[:3]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "source": entry.source.title,
            "date": entry.published,
            "type": "NEWS"
        })
    return articles

def main():
    # 1. Get the "Fact of the Day"
    daily_fact = {
        "title": random.choice(marketing_facts),
        "link": "#",
        "source": "Daily Insight",
        "date": datetime.now().strftime("%a, %d %b"),
        "type": "FACT"
    }

    # 2. Fetch Live Google News
    print("Fetching Digital Marketing News...")
    digital_news = fetch_google_news("Digital Marketing Trends India")

    print("Fetching Brand Marketing News...")
    brand_news = fetch_google_news("Brand Strategy India")

    print("Fetching AI Marketing News...")
    ai_news = fetch_google_news("Artificial Intelligence Marketing Tools")

    # 3. Combine
    all_content = [daily_fact] + digital_news + brand_news + ai_news

    # 4. Save
    with open('news.json', 'w') as f:
        json.dump(all_content, f, indent=4)
    print(f"Successfully saved {len(all_content)} insights.")

if __name__ == "__main__":
    main()
