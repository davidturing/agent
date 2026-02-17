import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_USER = "davidturing"
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USER}/events/public"
OUTPUT_FILE = "skills/self-learning-agent/data/raw/github_events.json"

def fetch_github_events():
    """Fetch recent public events for the GitHub user."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        print("Using GitHub Token.")
    else:
        print("Running without GitHub Token (limited rate).")

    try:
        response = requests.get(GITHUB_API_URL, headers=headers)
        response.raise_for_status()
        events = response.json()
        
        # Simple extraction of relevant data
        processed_events = []
        for event in events[:5]: # Top 5 recent events
            event_type = event.get("type", "Unknown")
            repo_name = event.get("repo", {}).get("name", "Unknown")
            created_at = event.get("created_at", "")
            
            payload = event.get("payload", {})
            description = ""
            
            if event_type == "PushEvent":
                commits = payload.get("commits", [])
                description = f"Pushed {len(commits)} commits: " + ", ".join([c.get("message", "") for c in commits])
            elif event_type == "CreateEvent":
                description = f"Created {payload.get('ref_type')} {payload.get('ref')}"
            elif event_type == "WatchEvent":
                description = "Starred the repository"
            elif event_type == "IssueCommentEvent":
                description = f"Commented on issue: {payload.get('comment', {}).get('body', '')[:50]}..."
            else:
                description = json.dumps(payload)[:100]

            processed_events.append({
                "source": "github",
                "type": event_type,
                "repo": repo_name,
                "timestamp": created_at,
                "content": description,
                "raw_url": f"https://github.com/{repo_name}"
            })

        # Save to file
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(processed_events, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully fetched {len(processed_events)} events from GitHub.")
        return processed_events

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub events: {e}")
        return []

def fetch_self_code():
    """Read own source code to understand current capabilities and methods."""
    source_dir = os.path.dirname(os.path.abspath(__file__))
    code_summary = []
    
    for filename in os.listdir(source_dir):
        if filename.endswith(".py"):
            with open(os.path.join(source_dir, filename), "r", encoding="utf-8") as f:
                content = f.read()
                code_summary.append(f"### File: {filename}\n```python\n{content}\n```")
    
    # Save self-reflection data
    output_path = "skills/self-learning-agent/data/raw/self_code.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(code_summary))
    
    print(f"Self-reflection: Read {len(code_summary)} source files.")

if __name__ == "__main__":
    fetch_github_events()
    fetch_self_code()
