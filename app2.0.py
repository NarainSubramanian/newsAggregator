import feedparser
import os
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
mongodb_uri = os.getenv("MONGODB_URI")

# MongoDB connection setup
client = MongoClient(mongodb_uri)  # Use the MongoDB URI from the .env file
db = client["ANT"]
collection = db["test"]

# Define tech news RSS feed URLs
RSS_FEED_URLS = [
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://www.theverge.com/rss/index.xml",
    "https://hnrss.org/frontpage"
]

# FastAPI app instance
app = FastAPI()

class Article(BaseModel):
    title: str
    timestamp: str
    content: Optional[str] = None

def fetch_articles_from_feed(feed_url):
    """Fetch articles from a single RSS feed."""
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        article = {
            '_id': entry.id,  # Use the unique RSS feed ID as MongoDB's _id
            'title': entry.title,
            'link': entry.link,
            'published_date': entry.published,
            'summary': entry.summary
        }
        articles.append(article)
    return articles

def save_articles(articles):
    """Save new articles to MongoDB, skipping duplicates based on _id."""
    for article in articles:
        if not collection.find_one({"_id": article['_id']}):
            collection.insert_one(article)

def fetch_and_save_articles():
    """Fetch and save articles from all RSS feed URLs."""
    for feed_url in RSS_FEED_URLS:
        articles = fetch_articles_from_feed(feed_url)
        save_articles(articles)

@app.on_event("startup")
async def startup_event():
    """Run fetch_and_save_articles() on startup."""
    fetch_and_save_articles()

@app.post("/fetch/")
async def fetch_articles(background_tasks: BackgroundTasks):
    """Fetches articles from RSS feeds and saves to MongoDB."""
    background_tasks.add_task(fetch_and_save_articles)
    return {"message": "Fetching articles in the background"}

@app.get("/articles/", response_model=List[Article])
async def get_articles(timestamp: str):
    """Fetch articles from MongoDB published after the given timestamp."""
    try:
        timestamp_dt = datetime.fromisoformat(timestamp)  # Expecting ISO format: YYYY-MM-DDTHH:MM:SS
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format. Use ISO format: YYYY-MM-DDTHH:MM:SS")

    # Query articles published after the given timestamp
    articles = list(collection.find({"published_date": {"$gt": timestamp}}))
    
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found after the given timestamp.")

    # Format the result to match response model
    result = [{"title": article['title'], "timestamp": article['published_date'], "content": article.get('summary')} for article in articles]
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
