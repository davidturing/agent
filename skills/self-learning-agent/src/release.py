import os
import datetime
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "davidturing"
REPO_NAME = "agent"
INSIGHTS_DIR = "skills/self-learning-agent/data/insights"

def create_github_release(tag_name, release_title, release_body):
    """Create a new release on GitHub."""
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN not found. Cannot publish release.")
        return False

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    data = {
        "tag_name": tag_name,
        "target_commitish": "main", # Or the branch you want to tag
        "name": release_title,
        "body": release_body,
        "draft": False,
        "prerelease": False,
        "generate_release_notes": False 
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ Successfully created release: {response.json().get('html_url')}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error publishing release to GitHub: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        return False

def get_latest_log_content():
    """Read the latest generated learning log."""
    import glob
    list_of_files = glob.glob(f"{INSIGHTS_DIR}/*.md")
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, "r", encoding="utf-8") as f:
        return f.read()

def main():
    print("--- 🚀 David Agent Release Module ---")
    
    content = get_latest_log_content()
    if not content:
        print("No insights log found to release.")
        return

    # Check if this log contains "Self-Reflection" (Evolution)
    if "Self-Reflection & Methodology" not in content:
        print("No self-evolution detected in latest log. Skipping release.")
        return

    # Extract version info
    date_str = datetime.date.today().isoformat()
    # Use timestamp for uniqueness in case of multiple runs per day
    timestamp = datetime.datetime.now().strftime("%H%M")
    tag_name = f"evolution-{date_str}-{timestamp}"
    
    # Extract title from content or use default
    title_line = content.split('\n')[0].replace("# ", "")
    release_title = f"David Agent Evolution: {date_str}"
    
    # Add signature
    release_body = content + "\n\n---\n*Automated Release by David Agent*"

    create_github_release(tag_name, release_title, release_body)

if __name__ == "__main__":
    main()
