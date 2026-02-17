import feedparser
import logging
from datetime import datetime
import time

logger = logging.getLogger(__name__)

DEFAULT_RSS_URL = "https://blog.camilobernal.dev/rss.xml"

def fetch_blog_posts(url=DEFAULT_RSS_URL, max_items=3):
    """
    Fetches the latest blog posts from the RSS feed.
    """
    try:
        logger.info(f"Fetching RSS feed from {url}...")
        feed = feedparser.parse(url)

        if feed.bozo:
            logger.warning(f"Potential error parsing RSS feed: {feed.bozo_exception}")
            # Continue if entries are present despite the error (common with minor XML issues)
            if not feed.entries:
                return []

        posts = []
        for entry in feed.entries[:max_items]:
            # Format date
            date_str = "Unknown Date"
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                date_str = time.strftime("%Y-%m-%d", entry.published_parsed)
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                date_str = time.strftime("%Y-%m-%d", entry.updated_parsed)

            posts.append({
                "title": entry.title,
                "link": entry.link,
                "date": date_str
            })

        logger.info(f"Fetched {len(posts)} posts.")
        return posts

    except Exception as e:
        logger.error(f"Error fetching blog posts: {e}")
        return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(fetch_blog_posts())
