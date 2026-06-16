import feedparser
import json
import requests
import re
from datetime import datetime

# --- 1. CONFIGURATION ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

FEEDS = {
    "MARKETING": "https://news.google.com/rss/search?q=Marketing+Strategy+India&hl=en-IN&gl=IN&ceid=IN:en",
    "ECOMMERCE": "https://news.google.com/rss/search?q=E-commerce+Trends+India&hl=en-IN&gl=IN&ceid=IN:en"
}

# --- 2. PREMIUM BRAND STORY DATABASE (12 Stories) ---
BRAND_STORIES = [
    {"brand": "Zomato", "campaign": "The 'Mood' Notification", "story": "Instead of generic 'Hungry?' notifications, Zomato used AI to predict user mood based on weather and time. A rainy Tuesday automatically triggered 'Chai & Pakoda' prompts.", "lesson": "Hyper-contextual triggers beat generic personalization.", "seed": "zomato1"},
    {"brand": "Cred", "campaign": "Indiranagar Ka Gunda", "story": "Cred purposefully used 'anti-casting'—putting a historically calm celebrity (Rahul Dravid) in an angry, chaotic role. This contrast created instant, viral meme material.", "lesson": "Disruption happens when you break an established archetype.", "seed": "cred2"},
    {"brand": "Nike", "campaign": "Winning Isn't For Everyone", "story": "In 2025, Nike moved away from 'inclusive' messaging back to 'exclusive' grit. They celebrated the ruthless obsession required to win, alienating some to deeply delight their core athletes.", "lesson": "Polarizing messaging builds stronger tribes than neutral messaging.", "seed": "nike3"},
    {"brand": "Spotify", "campaign": "Wrapped: The 'Roast'", "story": "Spotify didn't just show data; they assigned a 'Sound Town' and 'Vampire' persona. They playfully roasted users, gamifying data to make sharing a cultural status symbol.", "lesson": "Data is boring. Data identity is viral.", "seed": "spotify4"},
    {"brand": "Liquid Death", "campaign": "Murder Your Thirst", "story": "They took the world's most boring product (water), put it in an aluminum tallboy can that looks like craft beer, and used heavy-metal marketing to make hydration cool.", "lesson": "Packaging and attitude can differentiate a pure commodity.", "seed": "liquid5"},
    {"brand": "Oatly", "campaign": "The Meta-Billboard", "story": "Oatly ran billboards saying 'We spent a lot of money on this billboard to tell you about oat milk.' It broke the fourth wall of advertising, treating the consumer like an insider.", "lesson": "Self-referential transparency builds instant trust.", "seed": "oatly6"},
    {"brand": "Zepto", "campaign": "The 10-Minute Claim", "story": "Instead of vague promises like 'fast delivery', Zepto built their entire brand around a specific, measurable number (10 minutes) and backed it with a countdown timer.", "lesson": "Specific promises always outperform generalized claims.", "seed": "zepto7"},
    {"brand": "Dove", "campaign": "Reverse Digital Distortion", "story": "Dove actively campaigned against the 'Bold Glamour' AI filter on TikTok, urging users to turn their backs to the camera to protest synthetic beauty standards.", "lesson": "Taking a stand against a platform trend can win immense loyalty.", "seed": "dove8"},
    {"brand": "Patagonia", "campaign": "Don't Buy This Jacket", "story": "On Black Friday, Patagonia ran a full-page ad telling people NOT to buy their products unless absolutely necessary, highlighting the environmental cost of consumerism.", "lesson": "Anti-marketing is the ultimate form of brand authenticity.", "seed": "patagonia9"},
    {"brand": "Burger King", "campaign": "The Moldy Whopper", "story": "To prove they removed artificial preservatives, Burger King launched an ad campaign showing their flagship burger rotting and covered in mold over 34 days.", "lesson": "Ugly truths are more memorable than pretty lies.", "seed": "bk10"},
    {"brand": "Duolingo", "campaign": "Unhinged Mascot Marketing", "story": "Instead of polishing their corporate image, Duolingo let their owl mascot trend on TikTok by participating in pop-culture drama and playfully threatening users to do their lessons.", "lesson": "Gen Z prefers corporate self-awareness over corporate professionalism.", "seed": "duo11"},
    {"brand": "Airbnb", "campaign": "Belong Anywhere", "story": "Airbnb stopped marketing 'cheap places to stay' and started marketing 'living like a local'. They shifted the focus from the utility of the room to the identity of the traveler.", "lesson": "Sell the transformation, not the transaction.", "seed": "airbnb12"}
]

# --- 3. EXPANDED LEARNING ZONE ---
LEARNING_BRAND = [
    {"topic": "De-Influencing", "desc": "The trend where creators tell followers what *not* to buy. Brands must focus on product durability over hype."},
    {"topic": "Sonic Branding", "desc": "Netflix's 'Ta-dum' is worth millions. Brands are now trademarking 3-second audio cues for a screenless future."},
    {"topic": "Zero-Party Data", "desc": "Data a customer intentionally shares with a brand (e.g., via a quiz) is replacing cookies as the gold standard of targeting."}
]

LEARNING_ECOM = [
    {"topic": "Visual Search", "desc": "Gen Z is searching with images (Google Lens), not text. SEO now requires high-res, labeled product photography."},
    {"topic": "Agentic Commerce", "desc": "AI bots are starting to negotiate and buy items on behalf of humans. Marketers must optimize for AI buyers."},
    {"topic": "Returnless Refunds", "desc": "Amazon/Walmart now refund cheap items without asking for a return to save shipping costs. A logic shift for logistics."}
]

QUIZ_BANK = [
    {"q": "What is 'Share of Voice' (SOV)?", "options": ["Brand visibility vs competitors", "Total social shares", "Volume of audio ads"], "a": 0},
    {"q": "What does 'ROAS' stand for?", "options": ["Return on Ad Spend", "Rate of Active Sales", "Revenue on Asset Shares"], "a": 0},
    {"q": "What is a 'Dark Post'?", "options": ["Unpublished targeted social ad", "Negative brand review", "Night-mode content"], "a": 0}
]

def clean_html(raw_html):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', raw_html)[:120] + "..."

def fetch_google_news(url, category):
    try:
        feed = feedparser.parse(requests.get(url, headers=HEADERS, timeout=10).content)
        return [{"title": e.title, "link": e.link, "source": getattr(e, 'source', type('obj', (object,), {'title': 'News'})).title, "category": category} for e in feed.entries[:4]]
    except: return []

def main():
    day_of_year = datetime.now().timetuple().tm_yday
    
    data = {
        "date": datetime.now().strftime("%A, %d %B %Y"),
        "story": BRAND_STORIES[day_of_year % len(BRAND_STORIES)],
        "news": fetch_google_news(FEEDS["MARKETING"], "Strategy") + fetch_google_news(FEEDS["ECOMMERCE"], "Retail"),
        "learning": {
            "brand": LEARNING_BRAND[day_of_year % len(LEARNING_BRAND)], 
            "ecom": LEARNING_ECOM[day_of_year % len(LEARNING_ECOM)]
        },
        "quiz": QUIZ_BANK[day_of_year % len(QUIZ_BANK)]
    }

    with open('news.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Premium Feed Updated.")

if __name__ == "__main__":
    main()
