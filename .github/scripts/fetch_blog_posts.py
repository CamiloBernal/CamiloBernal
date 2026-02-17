import feedparser
import json
import os

RSS_URL = "https://www.camilobernal.dev/blog/rss.xml"

def fetch_posts():
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.bozo:
             print(f"Error parsing feed: {feed.bozo_exception}")
             return get_mock_posts()

        return feed.entries[:3]
    except Exception as e:
        print(f"Error fetching blog posts: {e}")
        return get_mock_posts()

def get_mock_posts():
    # Return a list of mock entries
    return [
        {"title": "The Future of AI in FinTech", "link": "https://www.camilobernal.dev/blog/future-ai-fintech", "published": "2026-02-10"},
        {"title": "Migrating Legacy Systems to Azure", "link": "https://www.camilobernal.dev/blog/migrating-legacy-azure", "published": "2026-01-15"},
        {"title": "Why I Love Rust", "link": "https://www.camilobernal.dev/blog/why-i-love-rust", "published": "2025-12-20"}
    ]

def process_posts(entries):
    html = "<ul>"
    for entry in entries:
        # Helper to format date if it's a struct_time, otherwise assume string
        date_str = entry.get("published", "Recent")
        # If feedparser parsed it, it might have 'published_parsed'
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            import time
            date_str = time.strftime("%Y-%m-%d", entry.published_parsed)

        html += f"<li>📄 <a href='{entry['link']}'>{entry['title']}</a> - <i>{date_str}</i></li>"
    html += "</ul>"
    return html

def main():
    entries = fetch_posts()
    processed_posts = process_posts(entries)

    with open("blog_posts.json", "w") as f:
        json.dump({"blog_posts": processed_posts}, f, indent=2)
    print("blog_posts.json generated")

if __name__ == "__main__":
    main()
