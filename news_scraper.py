import feedparser
import json
import random
import requests
import re
from datetime import datetime

# --- 1. CONFIGURATION ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# RELIABLE Google News RSS Feeds (These never fail)
FEEDS = {
    "MARKETING": "https://news.google.com/rss/search?q=Marketing+Strategy+India&hl=en-IN&gl=IN&ceid=IN:en",
    "ECOMMERCE": "https://news.google.com/rss/search?q=E-commerce+Trends+India&hl=en-IN&gl=IN&ceid=IN:en"
}

# --- 2. BRAND STORY DATABASE (The "Success Stories") ---
# These rotate daily to give you a fresh case study every time.
BRAND_STORIES = [
    {
        "brand": "Zomato",
        "campaign": "The 'Mood' Notification Strategy",
        "story": "Instead of generic 'Hungry?' notifications, Zomato used AI to predict user mood based on weather and time. A rainy Tuesday triggered 'Chai & Pakoda' prompts.",
        "lesson": "Hyper-contextual triggers beat generic personalization."
    },
    {
        "brand": "Cred",
        "campaign": "The 'Indiranagar Ka Gunda' Effect",
        "story": "Cred purposefully used 'anti-casting'—putting calm celebrities (like Rahul Dravid) in angry roles. This created instant meme material.",
        "lesson": "Disruption happens when you break a celebrity's established archetype."
    },
    {
        "brand": "Nike",
        "campaign": "Winning Isn't For Everyone",
        "story": "In 2025, Nike moved away from 'inclusive' messaging back to 'exclusive' grit. They celebrated the obsession required to win, alienating some to delight their core athletes.",
        "lesson": "Polarizing messaging builds stronger tribes than neutral messaging."
    },
    {
        "brand": "Spotify",
        "campaign": "Wrapped 2025: The 'Roast'",
        "story": "Spotify didn't just show data; they assigned a 'Sound Town' and 'Vampire' persona. They gamified user data to make sharing a status symbol.",
        "lesson": "Data is boring. Data identity is viral."
    }
]

# --- 3. LEARNING ZONE TOPICS ---
LEARNING_TOPICS = {
    "BRAND": [
        {"topic": "De-Influencing", "desc": "The trend where creators tell followers what *not* to buy. Brands must focus on product durability over hype."},
        {"topic": "Sonic Branding", "desc": "Netflix's 'Ta-dum' is worth millions. Brands are now trademarking 3-second audio cues for a screenless future."}
    ],
    "ECOMMERCE": [
        {"topic": "Visual Search", "desc": "Gen Z is searching with images (Google Lens), not text. SEO now requires high-res, labeled product photography."},
        {"topic": "Returnless Refunds", "desc": "Amazon/Walmart now refund cheap items without asking for a return to save shipping costs. A logic shift for logistics."}
    ]
}

QUIZ_BANK = [
    {"q": "What is 'Share of Voice' (SOV)?", "options": ["Your brand's visibility vs competitors", "Total social shares", "Volume of audio ads"], "a": 0},
    {"q": "In 2026, 'Cookie-less' marketing relies on?", "options": ["First-Party Data", "Third-Party Data", "Spyware"], "a": 0},
    {"q": "What is a 'Dark Post'?", "options": ["Unpublished social ad", "Negative review", "Night-mode content"], "a": 0}
]

# --- 4. FUNCTIONS ---
def clean_html(raw_html):
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', raw_html)
    return text[:120] + "..." if len(text) > 120 else text

def fetch_google_news(url, category):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        feed = feedparser.parse(response.content)
        articles = []
        for entry in feed.entries[:4]: # Top 4
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "source": entry.source.title if hasattr(entry, 'source') else "Google News",
                "date": entry.published,
                "category": category
            })
        return articles
    except:
        return []

def main():
    # 1. Fetch Reliable News
    news_marketing = fetch_google_news(FEEDS["MARKETING"], "Strategy")
    news_ecom = fetch_google_news(FEEDS["ECOMMERCE"], "Retail")
    
    # 2. Pick Random Content
    story = random.choice(BRAND_STORIES)
    learn_brand = random.choice(LEARNING_TOPICS["BRAND"])
    learn_ecom = random.choice(LEARNING_TOPICS["ECOMMERCE"])
    quiz = random.choice(QUIZ_BANK)
    
    data = {
        "date": datetime.now().strftime("%d %b, %Y"),
        "story": story,
        "news": news_marketing + news_ecom,
        "learning": {"brand": learn_brand, "ecom": learn_ecom},
        "quiz": quiz
    }

    with open('news.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Intelligence Feed Updated.")

if __name__ == "__main__":
    main()
