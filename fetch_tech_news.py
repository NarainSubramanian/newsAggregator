import feedparser
from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://narainsubramanium007:p90TQltQSjSA2jkj@cluster0.i2e1h.mongodb.net/ANT?retryWrites=true&w=majority&appName=Cluster0")  
db = client["ANT"]
collection = db["test"]

# List of tech news RSS feed URLs
RSS_FEED_URLS = [
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://www.theverge.com/rss/index.xml",
    "https://hnrss.org/frontpage"
    # Add more feeds here as needed
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
    new_articles_count = 0

    for article in articles:
        # Insert the article if it doesn't already exist in the collection
        if not collection.find_one({"_id": article['_id']}):
            collection.insert_one(article)
            new_articles_count += 1

    print(f"Saved {new_articles_count} new articles to the database.")

def main():
    for feed_url in RSS_FEED_URLS:
        print(f"Fetching articles from {feed_url}...")
        articles = fetch_articles_from_feed(feed_url)
        save_articles(articles)

if __name__ == "__main__":
    main()
