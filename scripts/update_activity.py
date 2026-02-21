"""
update_activity.py
Fetches the latest public GitHub events for CamiloBernal and injects them into README.md.

Environment variables:
    GH_TOKEN: GitHub Personal Access Token (required for higher rate limits)
    GITHUB_USERNAME: GitHub username to fetch events for (default: CamiloBernal)
"""

import os
import sys
import time
import datetime
import requests

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "CamiloBernal")
GH_TOKEN = os.environ.get("GH_TOKEN", "")
README_PATH = "README.md"
START_MARKER = "<!-- ACTIVITY_START -->"
END_MARKER = "<!-- ACTIVITY_END -->"
FALLBACK_CONTENT = "⏳ Cargando actividad reciente... Vuelve pronto."
MAX_EVENTS = 5
MAX_RETRIES = 3
TIMEOUT_SECONDS = 15
RATE_LIMIT_THRESHOLD = 10

GITHUB_EVENTS_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public?per_page=30"


def get_headers() -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "CamiloBernal-README-Bot/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if GH_TOKEN:
        headers["Authorization"] = f"Bearer {GH_TOKEN}"
    return headers


def relative_time(timestamp_str: str) -> str:
    """Return human-readable relative time from ISO8601 timestamp."""
    try:
        dt = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - dt
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return "hace un momento"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"hace {minutes} min"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"hace {hours}h"
        elif seconds < 604800:
            days = seconds // 86400
            return f"hace {days} día{'s' if days > 1 else ''}"
        else:
            weeks = seconds // 604800
            return f"hace {weeks} semana{'s' if weeks > 1 else ''}"
    except Exception:
        return "recientemente"


def format_event(event: dict) -> str | None:
    """Format a single GitHub event into a Markdown line."""
    event_type = event.get("type", "")
    repo = event.get("repo", {})
    repo_name = repo.get("name", "unknown/repo")
    repo_url = f"https://github.com/{repo_name}"
    created_at = event.get("created_at", "")
    rel_time = relative_time(created_at)
    payload = event.get("payload", {})

    if event_type == "PushEvent":
        commits = payload.get("commits", [])
        count = len(commits)
        if count == 0:
            return None
        commit_word = "commit" if count == 1 else "commits"
        return f"- 💻 Pushed {count} {commit_word} to **[{repo_name}]({repo_url})** — *{rel_time}*"

    elif event_type == "PullRequestEvent":
        action = payload.get("action", "")
        pr = payload.get("pull_request", {})
        pr_title = pr.get("title", "PR")
        pr_url = pr.get("html_url", repo_url)
        if action not in ("opened", "closed", "merged"):
            return None
        action_label = "mergeado" if (action == "closed" and pr.get("merged")) else action
        return f"- 🔀 PR *{action_label}*: **[{pr_title[:60]}]({pr_url})** en [{repo_name}]({repo_url}) — *{rel_time}*"

    elif event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "")
        ref = payload.get("ref", "")
        if ref_type == "tag" and ref:
            return f"- 🏷️ Released **{ref}** en **[{repo_name}]({repo_url})** — *{rel_time}*"
        elif ref_type == "repository":
            return f"- 📁 Creó repositorio **[{repo_name}]({repo_url})** — *{rel_time}*"
        return None

    elif event_type == "WatchEvent":
        return f"- ⭐ Dio una estrella a **[{repo_name}]({repo_url})** — *{rel_time}*"

    elif event_type == "ForkEvent":
        return f"- 🍴 Hizo fork de **[{repo_name}]({repo_url})** — *{rel_time}*"

    elif event_type == "IssuesEvent":
        action = payload.get("action", "")
        issue = payload.get("issue", {})
        issue_title = issue.get("title", "Issue")[:60]
        issue_url = issue.get("html_url", repo_url)
        if action in ("opened", "closed"):
            return f"- 🐛 Issue *{action}*: **[{issue_title}]({issue_url})** — *{rel_time}*"
        return None

    return None


def fetch_events_with_retry() -> list:
    """Fetch GitHub events with exponential backoff retry."""
    delay = 2
    last_exception = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Fetching GitHub events (attempt {attempt}/{MAX_RETRIES})...")
            response = requests.get(GITHUB_EVENTS_URL, headers=get_headers(), timeout=TIMEOUT_SECONDS)

            remaining = int(response.headers.get("X-RateLimit-Remaining", 999))
            if remaining < RATE_LIMIT_THRESHOLD:
                print(f"Warning: GitHub API rate limit low ({remaining} remaining). Skipping update.", file=sys.stderr)
                return []

            response.raise_for_status()
            events = response.json()
            print(f"Fetched {len(events)} events successfully.")
            return events
        except Exception as exc:
            last_exception = exc
            print(f"Attempt {attempt} failed: {exc}", file=sys.stderr)
            if attempt < MAX_RETRIES:
                print(f"Retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
    raise last_exception


def build_activity_section(events: list) -> str:
    """Format events into a Markdown section."""
    lines = []
    for event in events:
        formatted = format_event(event)
        if formatted:
            lines.append(formatted)
        if len(lines) >= MAX_EVENTS:
            break

    if not lines:
        return FALLBACK_CONTENT

    tz = datetime.timezone(datetime.timedelta(hours=-5))
    now_str = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M COT")
    lines.append(f"\n🕐 Actualizado: {now_str}")
    return "\n".join(lines)


def inject_into_readme(content: str, new_section: str) -> str:
    """Replace content between start and end markers."""
    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)
    if start_idx == -1 or end_idx == -1:
        print("Activity markers not found in README. Skipping injection.", file=sys.stderr)
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
        events = fetch_events_with_retry()
    except Exception as exc:
        print(f"Failed to fetch GitHub events after all retries: {exc}", file=sys.stderr)
        print("Keeping existing README content unchanged.")
        sys.exit(0)

    if not events:
        print("No events returned. Keeping existing README content.")
        sys.exit(0)

    new_section = build_activity_section(events)
    updated_content = inject_into_readme(readme_content, new_section)

    if updated_content == readme_content:
        print("No changes detected in README activity section.")
        sys.exit(0)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("README updated successfully with latest GitHub activity.")


if __name__ == "__main__":
    main()
