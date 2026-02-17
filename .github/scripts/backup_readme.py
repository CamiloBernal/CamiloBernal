import shutil
import os
import datetime

BACKUP_DIR = ".github/backups"
README_FILE = "README.md"

def backup_readme():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    if not os.path.exists(README_FILE):
        print("README.md not found, skipping backup")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(BACKUP_DIR, f"README_{timestamp}.md")

    shutil.copy2(README_FILE, backup_file)
    print(f"Backup created at {backup_file}")

    # Cleanup old backups (keep last 30)
    files = sorted(os.listdir(BACKUP_DIR))
    if len(files) > 30:
        for f in files[:-30]:
            os.remove(os.path.join(BACKUP_DIR, f))
            print(f"Removed old backup {f}")

if __name__ == "__main__":
    backup_readme()
