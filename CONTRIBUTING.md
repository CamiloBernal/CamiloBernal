# Contributing to Camilo Bernal's Profile

Thank you for your interest in contributing to my profile repository! This README is auto-generated using Python scripts and GitHub Actions.

## How it works

1.  **Templates**: The `README.template.md` file contains the static structure and placeholders.
2.  **Scripts**: The `.github/scripts/` directory contains Python scripts to fetch data and generate the README.
    *   `fetch_github_stats.py`: Fetches GitHub stats using GraphQL.
    *   `fetch_blog_posts.py`: Fetches blog posts from RSS.
    *   `generate_readme.py`: Combines the template with the data.
3.  **Automation**: The `.github/workflows/update-readme.yml` workflow runs daily to update the content.

## Development

To run the scripts locally:

1.  Install dependencies:
    ```bash
    pip install -r .github/scripts/requirements.txt
    ```

2.  Set `GITHUB_TOKEN` environment variable (optional, for real data).

3.  Run the generation script:
    ```bash
    python .github/scripts/generate_readme.py
    ```

## Guidelines

*   Keep the UI in Spanish (ES-CO).
*   Keep the code and documentation in English (EN-US).
*   Follow the design system described in the PRD (Purple/Cyan theme).
