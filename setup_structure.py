import os

directories = [
    ".github/workflows",
    "src/scripts",
    "src/assets/icons",
    "src/assets/json"
]

files = [
    "README_template.md",
    "requirements.txt",
    ".github/workflows/update-profile.yml",
    "src/scripts/main.py",
    "src/scripts/fetch_stats.py",
    "src/scripts/fetch_blog.py",
    "src/scripts/generate_svg.py",
    "src/scripts/utils.py",
    "src/assets/json/cache.json"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

for file in files:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write("")
        print(f"Created file: {file}")
