import os
import requests
import logging

logger = logging.getLogger(__name__)

def fetch_project_stats(username, projects):
    """
    Fetches stars and forks for the given list of repositories.
    username: GitHub username
    projects: list of repo names
    """
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        logger.warning("GITHUB_TOKEN not found. Skipping GitHub API stats.")
        return {}

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    # Construct GraphQL query dynamically
    query_parts = []
    for project in projects:
        # GraphQL aliases cannot contain hyphens
        safe_name = project.replace("-", "_")
        query_parts.append(f"""
        {safe_name}: repository(name: "{project}") {{
          stargazerCount
          forkCount
          url
        }}
        """)

    query = f"""
    query {{
      user(login: "{username}") {{
        {''.join(query_parts)}
      }}
    }}
    """

    try:
        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return {}

            user_data = data.get("data", {}).get("user", {})
            if not user_data:
                logger.warning("No user data returned from GitHub API.")
                return {}

            stats = {}
            for project in projects:
                safe_name = project.replace("-", "_")
                repo_data = user_data.get(safe_name)
                if repo_data:
                    stats[project] = {
                        "stars": repo_data["stargazerCount"],
                        "forks": repo_data["forkCount"],
                        "url": repo_data["url"]
                    }
            return stats
        else:
            logger.error(f"GitHub API failed with status {response.status_code}: {response.text}")
            return {}
    except Exception as e:
        logger.error(f"Error fetching GitHub stats: {e}")
        return {}

if __name__ == "__main__":
    # Test execution
    logging.basicConfig(level=logging.INFO)
    stats = fetch_project_stats("camilobernal", ["platform-builder", "architype", "hololife"])
    print(stats)
