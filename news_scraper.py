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

# --- 2. EXPANDED BRAND STORY DATABASE ---
BRAND_STORIES = [
    {"brand": "Zomato", "campaign": "The 'Mood' Notification Strategy", "story": "Instead of generic 'Hungry?' notifications, Zomato used AI to predict user mood based on weather and time. A rainy Tuesday triggered 'Chai & Pakoda' prompts.", "lesson": "Hyper-contextual triggers beat generic personalization."},
    {"brand": "Cred", "campaign": "The 'Indiranagar Ka Gunda' Effect", "story": "Cred purposefully used 'anti-casting'—putting calm celebrities (like Rahul Dravid) in angry roles. This created instant meme material.", "lesson": "Disruption happens when you break an established archetype."},
    {"brand": "Nike", "campaign": "Winning Isn't For Everyone", "story": "Nike moved away from 'inclusive' messaging back to 'exclusive' grit. They celebrated the obsession required to win, alienating some to delight their core athletes.", "lesson": "Polarizing messaging builds stronger tribes than neutral messaging."},
    {"brand": "Spotify", "campaign": "Wrapped: The 'Roast'", "story": "Spotify didn't just show data; they assigned a 'Sound Town' and 'Vampire' persona. They gamified user data to make sharing a status symbol.", "lesson": "Data is boring. Data identity is viral."},
    {"brand": "Duolingo", "campaign": "Unhinged Mascot Marketing", "story": "Instead of polishing their corporate image, Duolingo let their owl mascot trend on TikTok by participating in pop-culture drama and playfully threatening users.", "lesson": "Gen Z prefers corporate self-awareness over corporate professionalism."},
    {"brand": "Blinkit", "campaign": "Print Out Anything", "story": "Blinkit capitalized on the 'Quick Commerce' boom by offering a 10-minute printout delivery service, solving an immediate high-friction problem for Indian households.", "lesson": "Utility is the ultimate brand builder."},
    {"brand": "Liquid Death", "campaign": "Murder Your Thirst", "story": "They took the most boring product (water), put it in an aluminum tallboy can that looks like beer, and used heavy-metal marketing.", "lesson": "Packaging and attitude can differentiate a commodity."},
    {"brand": "Oatly", "campaign": "The 'We Made This Ad' Meta-Campaign", "story": "Oatly ran billboards saying 'We spent a lot of money on this billboard to tell you about oat milk.' It broke the fourth wall of advertising.", "lesson": "Self-referential transparency builds instant trust."},
    {"brand": "Zepto", "campaign": "The 10-Minute Claim", "story": "Instead of vague promises, Zepto built their entire brand around a specific, measurable number (10 minutes) and backed it with a countdown timer on the app.", "lesson": "Specific promises outperform generalized claims."},
    {"brand": "Dove", "campaign": "Turn Your Back (Digital Distortion)", "story": "Dove actively campaigned against the 'Bold Glamour' AI filter on TikTok, urging users to turn their backs to the camera to protest synthetic beauty standards.", "lesson": "Taking a stand against a platform trend can win immense loyalty."}
]

# --- 3. EXPANDED LEARNING ZONE ---
LEARNING_BRAND = [
    {"topic": "De-Influencing", "desc": "The trend where creators tell followers what *not* to buy. Brands must focus on product durability over hype."},
    {"topic": "Sonic Branding", "desc": "Netflix's 'Ta-dum' is worth millions. Brands are now trademarking 3-second audio cues for a screenless future."},
    {"topic": "Synthetic Influencers", "desc": "AI-generated models (like Lil Miquela) are taking brand deals. They never sleep, never age, and don't cause PR scandals."},
    {"topic": "Zero-Party Data", "desc": "Data a customer intentionally shares with a brand (e.g., via a quiz) is replacing cookies as the gold standard of targeting."},
    {"topic": "Community-Led Growth", "desc": "Moving away from followers to 'members'. Brands are building private Discord/WhatsApp communities for their super-fans."}
]

LEARNING_ECOM = [
    {"topic": "Visual Search", "desc": "Gen Z is searching with images (Google Lens), not text. SEO now requires high-res, labeled product photography."},
    {"topic": "Returnless Refunds", "desc": "Amazon/Walmart now refund cheap items without asking for a return to save shipping costs. A logic shift for logistics."},
    {"topic": "Agentic Commerce", "desc": "AI bots are starting to negotiate and buy items on behalf of humans. Marketers must optimize for AI buyers."},
    {"topic": "Live Commerce", "desc": "The QVC model adapted for Instagram/TikTok. Live streaming shopping events drive massive FOMO and instant conversions."},
    {"topic": "Hyper-Personalized Pricing", "desc": "Using AI to offer dynamic pricing based on user behavior, time of day, and inventory levels in real-time."}
]

# --- 4. EXPANDED QUIZ BANK ---
QUIZ_BANK = [
    {"q": "What is 'Share of Voice' (SOV)?", "options": ["Brand visibility vs competitors", "Total social shares", "Volume of audio ads"], "a": 0},
    {"q": "What does 'ROAS' stand for?", "options": ["Return on Ad Spend", "Rate of Active Sales", "Revenue on Asset Shares"], "a": 0},
    {"q": "Which is an example of 'First-Party Data'?", "options": ["Email list signups", "Purchased lists", "Google Analytics general traffic"], "a": 0},
    {"q": "In Quick Commerce, what does 'AOV' mean?", "options": ["Average Order Value", "Active Online Visitors", "Annual Output Volume"], "a": 0},
    {"q": "What is a 'Dark Post'?", "options": ["Unpublished targeted social ad", "Negative brand review", "Night-mode content"], "a": 0},
    {"q": "What defines the 'Freemium' model?", "options": ["Free basic product, paid premium features", "Buy one get one free", "Free shipping on orders"], "a": 0},
    {"q": "What is 'Churn Rate'?", "options": ["Percentage of customers who stop using a product", "Speed of inventory turnover", "Rate of ad impressions"], "a": 0}
]

# --- 5. CORE LOGIC ---
def clean_html(raw_html):
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', raw_html)
    return text[:130] + "..." if len(text) > 130 else text

def fetch_google_news(url, category):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        feed = feedparser.parse(response.content)
        articles = []
        for entry in feed.entries[:4]: # Top 4
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "source": entry.source.title if hasattr(entry, 'source') else "Industry News",
                "date": entry.published,
                "category": category
            })
        return articles
    except:
        return []

def main():
    # 1. Fetch Real-Time News
    news_marketing = fetch_google_news(FEEDS["MARKETING"], "Strategy")
    news_ecom = fetch_google_news(FEEDS["ECOMMERCE"], "Retail")
    
    # 2. Daily Deterministic Selection (Changes every 24 hours based on calendar date)
    day_of_year = datetime.now().timetuple().tm_yday
    
    daily_story = BRAND_STORIES[day_of_year % len(BRAND_STORIES)]
    daily_brand_learn = LEARNING_BRAND[day_of_year % len(LEARNING_BRAND)]
    daily_ecom_learn = LEARNING_ECOM[day_of_year % len(LEARNING_ECOM)]
    daily_quiz = QUIZ_BANK[day_of_year % len(QUIZ_BANK)]
    
    # 3. Assemble Payload
    data = {
        "date": datetime.now().strftime("%A, %d %B %Y"),
        "story": daily_story,
        "news": news_marketing + news_ecom,
        "learning": {"brand": daily_brand_learn, "ecom": daily_ecom_learn},
        "quiz": daily_quiz
    }

    # 4. Save to JSON
    with open('news.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Intelligence Feed Updated for Day {day_of_year}.")

if __name__ == "__main__":
    main()
