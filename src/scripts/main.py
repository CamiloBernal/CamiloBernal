import os
import shutil
import jinja2
import logging
from datetime import datetime

# Add src/scripts to path if needed, but since we run from root usually
# imports should work if structured correctly or we adjust sys.path
import sys
sys.path.append(os.path.join(os.getcwd(), "src", "scripts"))

from fetch_blog import fetch_blog_posts
from fetch_stats import fetch_project_stats
from utils import load_cache, save_cache, safe_execute

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TEMPLATE_FILE = "README_template.md"
OUTPUT_FILE = "README.md"
USERNAME = "camilobernal"
PROJECTS = ["platform-builder", "architype", "hololife"]

def main():
    logger.info("Starting profile update...")

    # Load cache
    cache = load_cache()

    # Fetch Data with resilience
    logger.info("Fetching blog posts...")
    blog_posts = safe_execute(fetch_blog_posts, "blog_posts", cache)

    logger.info("Fetching project stats...")
    project_stats = safe_execute(fetch_project_stats, "project_stats", cache, USERNAME, PROJECTS)

    # Prepare context for Jinja2
    context = {
        "blog_posts": blog_posts,
        "project_stats": project_stats,
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    # Backup previous README
    if os.path.exists(OUTPUT_FILE):
        try:
            shutil.copy(OUTPUT_FILE, OUTPUT_FILE + ".bak")
            logger.info("Backed up previous README.md")
        except Exception as e:
            logger.warning(f"Failed to backup README.md: {e}")

    # Render Template
    try:
        logger.info("Rendering template...")
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            template_content = f.read()

        template = jinja2.Template(template_content)
        rendered_content = template.render(context)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(rendered_content)

        logger.info(f"Successfully generated {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        # If rendering fails, we might want to restore backup
        if os.path.exists(OUTPUT_FILE + ".bak"):
            shutil.copy(OUTPUT_FILE + ".bak", OUTPUT_FILE)
            logger.info("Restored backup due to rendering failure.")

    # Save Cache
    save_cache(cache)

if __name__ == "__main__":
    main()
