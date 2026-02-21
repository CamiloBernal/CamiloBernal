"""
update_blog_posts.py
Fetches the latest 3 blog posts from the RSS feed and injects them into README.md.

Environment variables:
    BLOG_RSS_URL: URL of the RSS feed (default: https://blog.camilobernal.dev/rss.xml)
"""

import os
import sys
import time
import datetime
import feedparser
import requests

BLOG_RSS_URL = os.environ.get("BLOG_RSS_URL", "https://blog.camilobernal.dev/rss.xml")
README_PATH = "README.md"
START_MARKER = "<!-- BLOG_START -->"
END_MARKER = "<!-- BLOG_END -->"
FALLBACK_CONTENT = "📖 [Lee mis artículos en blog.camilobernal.dev](https://blog.camilobernal.dev)"
MAX_POSTS = 3
MAX_RETRIES = 3
TIMEOUT_SECONDS = 10


def relative_date(published_parsed) -> str:
    """Return a human-readable relative date string."""
    if not published_parsed:
        return "recientemente"
    try:
        pub_dt = datetime.datetime(*published_parsed[:6], tzinfo=datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - pub_dt
        days = delta.days
        if days == 0:
            return "hoy"
        elif days == 1:
            return "ayer"
        elif days < 7:
            return f"hace {days} días"
        elif days < 30:
            weeks = days // 7
            return f"hace {weeks} semana{'s' if weeks > 1 else ''}"
        elif days < 365:
            months = days // 30
            return f"hace {months} mes{'es' if months > 1 else ''}"
        else:
            years = days // 365
            return f"hace {years} año{'s' if years > 1 else ''}"
    except Exception:
        return "recientemente"


def fetch_rss_with_retry(url: str) -> feedparser.FeedParserDict:
    """Fetch RSS feed with exponential backoff retry."""
    delay = 2
    last_exception = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Fetching RSS feed (attempt {attempt}/{MAX_RETRIES}): {url}")
            response = requests.get(url, timeout=TIMEOUT_SECONDS, headers={"User-Agent": "CamiloBernal-README-Bot/1.0"})
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            if feed.bozo and not feed.entries:
                raise ValueError(f"Feed parse error: {feed.bozo_exception}")
            print(f"Feed fetched successfully. Entries found: {len(feed.entries)}")
            return feed
        except Exception as exc:
            last_exception = exc
            print(f"Attempt {attempt} failed: {exc}", file=sys.stderr)
            if attempt < MAX_RETRIES:
                print(f"Retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
    raise last_exception


def format_posts(entries: list) -> str:
    """Format RSS entries into Markdown list items."""
    lines = []
    for entry in entries[:MAX_POSTS]:
        title = entry.get("title", "Sin título").strip()
        link = entry.get("link", "https://blog.camilobernal.dev").strip()
        pub = entry.get("published_parsed") or entry.get("updated_parsed")
        date_str = relative_date(pub)
        lines.append(f"- 📌 **[{title}]({link})** — *{date_str}*")
    return "\n".join(lines)


def inject_into_readme(content: str, new_section: str) -> str:
    """Replace content between start and end markers."""
    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)
    if start_idx == -1 or end_idx == -1:
        print("Markers not found in README. Skipping injection.", file=sys.stderr)
        return content
    before = content[: start_idx + len(START_MARKER)]
    after = content[end_idx:]
    return f"{before}\n{new_section}\n{after}"


def main():
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"README not found at {README_PATH}. Exiting.", file=sys.stderr)
        sys.exit(0)

    try:
        feed = fetch_rss_with_retry(BLOG_RSS_URL)
        if not feed.entries:
            print("No entries found in feed. Keeping existing content.", file=sys.stderr)
            sys.exit(0)
        new_section = format_posts(feed.entries)
    except Exception as exc:
        print(f"Failed to fetch/parse RSS after all retries: {exc}", file=sys.stderr)
        print("Keeping existing README content unchanged.")
        sys.exit(0)

    updated_content = inject_into_readme(readme_content, new_section)

    if updated_content == readme_content:
        print("No changes detected in README blog section.")
        sys.exit(0)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"README updated successfully with {min(len(feed.entries), MAX_POSTS)} blog posts.")


if __name__ == "__main__":
    main()
