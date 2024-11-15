import feedparser
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

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

# Main entry point for running the cron job
if __name__ == "__main__":
    fetch_and_save_articles()
