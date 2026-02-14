import feedparser
import json
import random
import re
import requests
from datetime import datetime
import time

# --- CONFIGURATION ---
# We use a real browser header to avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

FEEDS = {
    "GENERAL": "https://www.marketingdive.com/feeds/news/",
    "ECOMMERCE": "https://retail.economictimes.indiatimes.com/rss/topstories",
    "CONTENT": "https://contentmarketinginstitute.com/feed/",
    # Ads of the World YouTube Channel
    "BRAND_FILMS": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBNQC2_gtsQ3X_V-MvF3u1Q"
}

# --- QUIZ BANK ---
QUIZ_BANK = [
    {"q": "What is the primary goal of a 'Lead Magnet'?", "options": ["Collect contact info", "Make a direct sale", "Increase bounce rate"], "a": 0},
    {"q": "Which metric tracks the cost to acquire one paying customer?", "options": ["CAC", "LTV", "RPM"], "a": 0},
    {"q": "What does 'SERP' stand for?", "options": ["Search Engine Results Page", "System Error Recovery Plan", "Site Efficiency Rating Protocol"], "a": 0},
    {"q": "In email marketing, what is 'A/B Testing'?", "options": ["Comparing two versions", "Sending to all subscribers", "Testing spam filters"], "a": 0},
    {"q": "Which social platform is 'Threads' associated with?", "options": ["Instagram", "Twitter", "Snapchat"], "a": 0}
]

def fetch_feed_data(url):
    """Fetches raw feed data using requests to bypass blocking."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response.content
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def clean_summary(html_text):
    """Removes HTML tags."""
    if not html_text: return "Click to read full story."
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', html_text)
    return text[:120] + "..." if len(text) > 120 else text

def fetch_news(url, category):
    print(f"Fetching {category}...")
    raw_data = fetch_feed_data(url)
    if not raw_data: return []

    feed = feedparser.parse(raw_data)
    articles = []
    
    # Grab top 3 items
    for entry in feed.entries[:3]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": clean_summary(entry.summary if hasattr(entry, 'summary') else entry.title),
            "category": category,
            "type": "NEWS"
        })
    return articles

def fetch_videos(url):
    print("Fetching Brand Films...")
    raw_data = fetch_feed_data(url)
    if not raw_data: return []

    feed = feedparser.parse(raw_data)
    videos = []
    
    # Grab latest video
    for entry in feed.entries[:1]:
        # YouTube feeds sometimes hide the ID, usually found in the link or yt_videoid
        video_id = entry.yt_videoid if hasattr(entry, 'yt_videoid') else entry.link.split('=')[-1]
        videos.append({
            "title": entry.title,
            "video_id": video_id,
            "link": entry.link,
            "type": "VIDEO"
        })
    return videos

def main():
    # 1. Fetch Data
    general = fetch_news(FEEDS["GENERAL"], "General Marketing")
    ecom = fetch_news(FEEDS["ECOMMERCE"], "E-Commerce")
    content = fetch_news(FEEDS["CONTENT"], "Content Strategy")
    films = fetch_videos(FEEDS["BRAND_FILMS"])
    
    # 2. Pick Quiz
    daily_quiz = random.choice(QUIZ_BANK)
    
    # 3. Combine
    all_news = general + ecom + content
    
    # FALLBACK: If news is empty, add a placeholder so dashboard isn't blank
    if not all_news:
        all_news.append({
            "title": "System Update: Feeds are refreshing...",
            "link": "#",
            "summary": "Please check back in 1 hour.",
            "category": "System",
            "type": "NEWS"
        })

    final_data = {
        "date": datetime.now().strftime("%d %b, %Y"),
        "quiz": daily_quiz,
        "video": films[0] if films else None,
        "news": all_news
    }

    # 4. Save
    with open('news.json', 'w') as f:
        json.dump(final_data, f, indent=4)
    print("Dashboard Update Complete.")

if __name__ == "__main__":
    main()
