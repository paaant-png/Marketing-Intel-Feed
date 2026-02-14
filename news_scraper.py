import feedparser
import json
import random
import re
from datetime import datetime

# --- CONFIGURATION: RELIABLE RSS SOURCES ---
FEEDS = {
    "GENERAL": "https://www.marketingdive.com/feeds/news/",
    "ECOMMERCE": "https://www.retaildive.com/feeds/news/",
    "CONTENT": "https://contentmarketinginstitute.com/feed/",
    # YouTube RSS for 'Ads of the World' or similar creative channel
    "BRAND_FILMS": "https://www.youtube.com/feeds/videos.xml?channel_id=UCBNQC2_gtsQ3X_V-MvF3u1Q" 
}

# --- QUIZ BANK (Static for reliability) ---
QUIZ_BANK = [
    {"q": "What does SEO stand for?", "options": ["Search Engine Optimization", "Sales Engine Output", "Site Efficiency Order"], "a": 0},
    {"q": "Which metric measures the percentage of visitors who leave after one page?", "options": ["Bounce Rate", "Churn Rate", "Exit Velocity"], "a": 0},
    {"q": "In A/B testing, how many variables should you change at once?", "options": ["One", "Two", "As many as possible"], "a": 0},
    {"q": "What is the '4 P's' of marketing?", "options": ["Product, Price, Place, Promotion", "Plan, People, Process, Profit", "Power, Pitch, Play, Performance"], "a": 0},
    {"q": "Which platform is known for B2B marketing?", "options": ["LinkedIn", "TikTok", "Snapchat"], "a": 0}
]

def clean_summary(html_text):
    """Removes HTML tags to give clean text summaries."""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', html_text)
    return text[:150] + "..." if len(text) > 150 else text

def fetch_news(url, category):
    print(f"Fetching {category}...")
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:3]: # Top 3 per category
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": clean_summary(entry.summary) if hasattr(entry, 'summary') else "",
            "category": category,
            "type": "NEWS"
        })
    return articles

def fetch_videos(url):
    print("Fetching Brand Films...")
    feed = feedparser.parse(url)
    videos = []
    for entry in feed.entries[:1]: # Latest 1 Video
        # Extract YouTube ID
        video_id = entry.yt_videoid if hasattr(entry, 'yt_videoid') else entry.link.split('=')[-1]
        videos.append({
            "title": entry.title,
            "video_id": video_id,
            "link": entry.link,
            "type": "VIDEO"
        })
    return videos

def main():
    # 1. Fetch All Data
    general = fetch_news(FEEDS["GENERAL"], "Marketing")
    ecom = fetch_news(FEEDS["ECOMMERCE"], "E-Commerce")
    content = fetch_news(FEEDS["CONTENT"], "Content Strategy")
    films = fetch_videos(FEEDS["BRAND_FILMS"])
    
    # 2. Get Daily Quiz
    daily_quiz = random.choice(QUIZ_BANK)
    daily_quiz["type"] = "QUIZ"

    # 3. Combine Data
    final_data = {
        "date": datetime.now().strftime("%d %b, %Y"),
        "quiz": daily_quiz,
        "video": films[0] if films else None,
        "news": general + ecom + content
    }

    # 4. Save
    with open('news.json', 'w') as f:
        json.dump(final_data, f, indent=4)
    print("Dashboard Updated Successfully.")

if __name__ == "__main__":
    main()
