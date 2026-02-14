import feedparser
import json
import random
import re
import requests
from datetime import datetime

# --- 1. CONFIGURATION ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

FEEDS = {
    "GENERAL": "https://www.marketingdive.com/feeds/news/",
    "ECOMMERCE_NEWS": "https://retail.economictimes.indiatimes.com/rss/topstories",
    "BRAND_FILMS": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBNQC2_gtsQ3X_V-MvF3u1Q", # Ads of the World
    "BACKUP_FILMS": "https://www.youtube.com/feeds/videos.xml?channel_id=UCgl9rHDiUpPOAW94l-fisOg"  # Google Ads
}

# --- 2. LEARNING ZONE (Hardcoded 2026 Insights) ---
# We rotate these daily so the user learns something new every time.
LEARNING_TOPICS = {
    "BRAND": [
        {"topic": "The 'Doom Loop'", "desc": "A 2026 trend where CMOs lose influence by failing to prove brand ROI. Fix: Connect brand metrics to cash flow."},
        {"topic": "Authentic Societal Engagement", "desc": "Brands that move beyond 'performative activism' to real social impact are seeing 2x higher retention."},
        {"topic": "Micro-Drama Content", "desc": "Short, serialized video storytelling on TikTok/Reels is replacing static ads for Gen Z engagement."}
    ],
    "ECOMMERCE": [
        {"topic": "Agentic Commerce", "desc": "AI Agents (not humans) are starting to make buying decisions. Optimization must now target AI bots, not just people."},
        {"topic": "Zero-Click Search", "desc": "With AI answers (SearchGPT/Gemini), users don't click links. Brands must optimize for 'Answer Engine Optimization' (AEO)."},
        {"topic": "Quick Commerce 2.0", "desc": "The shift from 10-min grocery delivery to 30-min 'everything' delivery (electronics, fashion) is the new battleground."}
    ]
}

QUIZ_BANK = [
    {"q": "What is 'CAC' in marketing?", "options": ["Customer Acquisition Cost", "Click Analysis Chart", "Content Ad Campaign"], "a": 0},
    {"q": "Which metric matters most for 'Agentic Commerce'?", "options": ["Data Structure", "Visual Appeal", "Button Color"], "a": 0},
    {"q": "What is the 2026 trend 'Zero-Click'?", "options": ["Users get answers without clicking websites", "Buying without checkout", "Ads with no links"], "a": 0}
]

# --- 3. HELPER FUNCTIONS ---
def fetch_raw(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response.content if response.status_code == 200 else None
    except: return None

def clean_text(html):
    if not html: return ""
    text = re.sub(r'<[^>]+>', '', html)
    return text[:130] + "..." if len(text) > 130 else text

def get_feed(url, category, limit=3):
    raw = fetch_raw(url)
    if not raw: return []
    feed = feedparser.parse(raw)
    return [{
        "title": e.title,
        "link": e.link,
        "summary": clean_text(e.summary if hasattr(e, 'summary') else e.title),
        "category": category
    } for e in feed.entries[:limit]]

def get_video(primary, backup):
    def parse(url):
        raw = fetch_raw(url)
        if not raw: return []
        feed = feedparser.parse(raw)
        videos = []
        for e in feed.entries[:1]:
            vid = e.yt_videoid if hasattr(e, 'yt_videoid') else e.link.split('=')[-1]
            videos.append({"title": e.title, "id": vid})
        return videos

    vids = parse(primary)
    if not vids: vids = parse(backup)
    return vids[0] if vids else None

# --- 4. MAIN EXECUTION ---
def main():
    # Fetch Feeds
    news_gen = get_feed(FEEDS["GENERAL"], "Brand News")
    news_ecom = get_feed(FEEDS["ECOMMERCE_NEWS"], "Retail Tech")
    video = get_video(FEEDS["BRAND_FILMS"], FEEDS["BACKUP_FILMS"])
    
    # Pick Learning Topics (Randomly select 1 from each category)
    learn_brand = random.choice(LEARNING_TOPICS["BRAND"])
    learn_ecom = random.choice(LEARNING_TOPICS["ECOMMERCE"])
    
    data = {
        "date": datetime.now().strftime("%d %b, %Y"),
        "video": video,
        "quiz": random.choice(QUIZ_BANK),
        "news_feed": news_gen,       # General Marketing News
        "ecom_feed": news_ecom,      # Dedicated E-com News
        "learning": {                # New Learning Zone Data
            "brand": learn_brand,
            "ecom": learn_ecom
        }
    }

    with open('news.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Intelligence Feed Updated.")

if __name__ == "__main__":
    main()
