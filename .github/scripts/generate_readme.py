import json
import datetime
import os

TEMPLATE_FILE = "README.template.md"
OUTPUT_FILE = "README.md"
STATS_FILE = "stats.json"
BLOG_FILE = "blog_posts.json"

def load_json(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found, returning empty dict")
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def main():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Template {TEMPLATE_FILE} not found!")
        return

    with open(TEMPLATE_FILE, "r") as f:
        template = f.read()

    stats = load_json(STATS_FILE)
    blog = load_json(BLOG_FILE)

    recent_activity = stats.get("recent_activity", "<ul><li>No recent activity found</li></ul>")
    blog_posts = blog.get("blog_posts", "<ul><li>No recent blog posts found</li></ul>")

    # Get current time in COT (UTC-5)
    # Using timezone-aware UTC now
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    cot_offset = datetime.timezone(datetime.timedelta(hours=-5))
    cot_now = utc_now.astimezone(cot_offset)
    last_updated = cot_now.strftime("%Y-%m-%d %H:%M COT")

    readme_content = template.replace("{{RECENT_ACTIVITY}}", recent_activity)
    readme_content = readme_content.replace("{{BLOG_POSTS}}", blog_posts)
    readme_content = readme_content.replace("{{LAST_UPDATED}}", last_updated)

    with open(OUTPUT_FILE, "w") as f:
        f.write(readme_content)

    print(f"{OUTPUT_FILE} generated successfully")

if __name__ == "__main__":
    main()
