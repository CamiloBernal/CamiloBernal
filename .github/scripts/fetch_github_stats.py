import os
import json
import requests
import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = "camilobernal"

def fetch_stats():
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not found, returning mock data")
        return get_mock_stats()

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    # GraphQL query for recent activity
    query = """
    query {
      user(login: "%s") {
        repositories(first: 5, orderBy: {field: UPDATED_AT, direction: DESC}, privacy: PUBLIC) {
          nodes {
            name
            url
            updatedAt
            description
            primaryLanguage {
              name
              color
            }
          }
        }
        contributionsCollection {
          commitContributionsByRepository(maxRepositories: 5) {
            repository {
              name
              url
            }
            contributions(first: 5) {
              totalCount
            }
          }
        }
      }
    }
    """ % USERNAME

    try:
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            print(f"Query failed to run by returning code of {request.status_code}. {query}")
            return get_mock_stats()
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return get_mock_stats()

def get_mock_stats():
    return {
        "data": {
            "user": {
                "repositories": {
                    "nodes": [
                        {
                            "name": "platform-builder",
                            "url": "https://github.com/camilobernal/platform-builder",
                            "updatedAt": datetime.datetime.now().isoformat(),
                            "description": "NoCode platform with semantic models",
                            "primaryLanguage": {"name": "TypeScript", "color": "#2b7489"}
                        },
                        {
                            "name": "architype",
                            "url": "https://github.com/camilobernal/architype",
                            "updatedAt": datetime.datetime.now().isoformat(),
                            "description": "IT Architecture Diagramming tool",
                            "primaryLanguage": {"name": "Python", "color": "#3572A5"}
                        }
                    ]
                }
            }
        }
    }

def process_activity(data):
    # Process the raw GraphQL data into a friendly list of strings
    activities = []

    if not data or "data" not in data or not data["data"]["user"]:
        return ["<ul><li>Updating activity...</li></ul>"]

    repos = data["data"]["user"]["repositories"]["nodes"]

    html = "<ul>"
    for repo in repos:
        date_str = repo["updatedAt"].split("T")[0]
        lang = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "Text"
        html += f"<li>⚡ Working on <a href='{repo['url']}'><b>{repo['name']}</b></a> ({lang}) - <i>{date_str}</i></li>"
    html += "</ul>"

    return html

def main():
    data = fetch_stats()
    processed_activity = process_activity(data)

    # Save to file
    with open("stats.json", "w") as f:
        json.dump({"recent_activity": processed_activity}, f, indent=2)
    print("stats.json generated")

if __name__ == "__main__":
    main()
