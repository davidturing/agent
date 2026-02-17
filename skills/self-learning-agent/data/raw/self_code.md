### File: ingest_x.py
```python
import os
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

X_ACCOUNTS_FILE = "skills/self-learning-agent/data/raw/x_accounts.json"
X_TWEETS_OUTPUT = "skills/self-learning-agent/data/raw/x_tweets.json"

def fetch_x_tweets():
    """Fetch latest tweets from curated X accounts using bird CLI."""
    if not os.path.exists(X_ACCOUNTS_FILE):
        print(f"Error: {X_ACCOUNTS_FILE} not found.")
        return []

    with open(X_ACCOUNTS_FILE, "r") as f:
        accounts = json.load(f)

    all_tweets = []
    
    # In a real production scenario, we'd loop through all, 
    # but for stability we might limit the number per run.
    for account in accounts[:5]: # Let's try the first 5 for now
        handle = account["handle"]
        print(f"Fetching tweets from @{handle}...")
        
        try:
            # Using bird search for specific user
            result = subprocess.run(
                ["bird", "search", f"from:{handle}", "-n", "3", "--json"],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            print(f"Return code: {result.returncode}")
                
        except Exception as e:
            print(f"Exception fetching @{handle}: {e}")

    # Save to file
    os.makedirs(os.path.dirname(X_TWEETS_OUTPUT), exist_ok=True)
    with open(X_TWEETS_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_tweets, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully fetched {len(all_tweets)} tweets from X.")
    return all_tweets

if __name__ == "__main__":
    fetch_x_tweets()

```

### File: ingest.py
```python
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

```

### File: release.py
```python
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

```

### File: brain_graph.py
```python
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = "skills/self-learning-agent/pageindex/knowledge"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_DEFAULT = os.getenv("MODEL_DEFAULT", "gemini-3-pro-preview")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_DEFAULT}:generateContent?key={GEMINI_API_KEY}"

def analyze_for_graph(text):
    """Use Gemini to extract entities and relations from text."""
    prompt = f"""
    Analyze the following technical content and extract entities and their relationships.
    Format the output as a JSON list of triples: [subject, relation, object].
    Also suggest a category and sub-topic for storage.
    
    Content: {text}
    
    Response format:
    {{
      "entities": ["entity1", "entity2"],
      "triples": [["entity1", "relation", "entity2"]],
      "category": "CategoryName",
      "topic": "SubTopicName",
      "summary": "Short summary"
    }}
    """
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        resp = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=15)
        if resp.status_code == 200:
            content = resp.json()['candidates'][0]['content']['parts'][0]['text']
            # Basic cleanup of markdown code blocks
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
    except Exception as e:
        print(f"Graph analysis failed: {e}")
    return None

def update_page_index(persona, analysis, raw_text):
    """Store knowledge in the PageIndex directory structure."""
    category = analysis.get("category", "General").replace(" ", "_")
    topic = analysis.get("topic", "Misc").replace(" ", "_")
    
    target_dir = os.path.join(BASE_DIR, persona, category, topic)
    os.makedirs(target_dir, exist_ok=True)
    
    # Save index.md
    index_path = os.path.join(target_dir, "index.md")
    mode = "a" if os.path.exists(index_path) else "w"
    
    with open(index_path, mode, encoding="utf-8") as f:
        if mode == "w":
            f.write(f"# {topic} (Category: {category})\n\n")
        
        f.write(f"## New Insight\n")
        f.write(f"- **Summary**: {analysis.get('summary')}\n")
        f.write(f"- **Relationships**:\n")
        for s, r, o in analysis.get("triples", []):
            f.write(f"  - {s} --({r})--> {o}\n")
        f.write("\n")

    print(f"PageIndex: Updated {index_path}")

def process_latest_x_data():
    x_raw = "skills/self-learning-agent/data/raw/x_tweets.json"
    if not os.path.exists(x_raw):
        return
        
    with open(x_raw, "r") as f:
        tweets = json.load(f)
        
    for tweet in tweets[:3]: # Process top 3 for stability
        text = tweet.get('text', '')
        persona = tweet.get('persona', 'Tech_Guru')
        
        print(f"Analyzing tweet for PageIndex...")
        analysis = analyze_for_graph(text)
        if analysis:
            update_page_index(persona, analysis, text)

if __name__ == "__main__":
    process_latest_x_data()

```

### File: release_github.py
```python
import subprocess
import os
import datetime

REPO_PATH = "/Users/zhaoqinhuang/david_project"
KNOWLEDGE_PATH = "skills/self-learning-agent/pageindex/knowledge"

def push_to_github():
    """Commit and push new knowledge to the GitHub repository."""
    print("\n[Stage 5] Syncing Knowledge to GitHub")
    
    try:
        # Check if there are changes in the knowledge directory
        status = subprocess.run(
            ["git", "status", "--short", KNOWLEDGE_PATH],
            capture_output=True, text=True, cwd=REPO_PATH
        )
        
        if not status.stdout.strip():
            print("No new knowledge to sync.")
            return

        # Add only the knowledge directory
        subprocess.run(["git", "add", KNOWLEDGE_PATH], cwd=REPO_PATH, check=True)
        
        # Commit with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"David Agent: Update Knowledge Graph - {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_message], cwd=REPO_PATH, check=True)
        
        # Push to the target knowledge repository (davidturing/agent)
        # Using the subtree strategy to only push the knowledge directory
        # Format: git subtree push --prefix=DIR REMOTE BRANCH
        print(f"Syncing knowledge to davidturing/agent...")
        result = subprocess.run(
            ["git", "subtree", "push", "--prefix", KNOWLEDGE_PATH, "knowledge", "main"],
            capture_output=True, text=True, cwd=REPO_PATH
        )
        
        if result.returncode == 0:
            print(f"Successfully pushed knowledge to davidturing/agent.")
        else:
            # Fallback to normal push if subtree fails (e.g. repo initialization)
            print(f"Subtree push failed, attempting standard push to 'knowledge' remote...")
            result = subprocess.run(["git", "push", "knowledge", "main"], capture_output=True, text=True, cwd=REPO_PATH)
            
        if result.returncode == 0:
            print("Sync complete.")
        else:
            print(f"Git push failed: {result.stderr}")
            
    except Exception as e:
        print(f"GitHub Sync failed: {e}")

if __name__ == "__main__":
    push_to_github()

```

### File: brain.py
```python
import os
import datetime
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
INSIGHTS_PATH = os.path.join(os.path.dirname(__file__), "../data/insights")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_DEFAULT = os.getenv("MODEL_DEFAULT", "gemini-3-pro-preview")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_DEFAULT}:generateContent?key={GEMINI_API_KEY}"

def generate_daily_log(insights):
    date_str = datetime.date.today().isoformat()
    content = f"# David Agent Lite Log - {date_str}\n\n"
    
    content += "## 🧠 Insights (HTTP Mode)\n"
    for item in insights:
        content += f"- **{item.get('category', 'General')}**: {item.get('summary')}\n"
    
    content += "\n---\n*Generated by David Agent (Slim Architecture)*"
    
    os.makedirs(INSIGHTS_PATH, exist_ok=True)
    filename = os.path.join(INSIGHTS_PATH, f"daily_log_{date_str}_lite.md")
    
    with open(filename, "w") as f:
        f.write(content)
        
    return filename

def analyze_text(text):
    """Analyze text using Gemini API directly (no heavy library)."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": f"Summarize this technical update into a single bullet point insight: {text}"}]
        }]
    }
    
    try:
        resp = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Extract text safely
            try:
                summary = data['candidates'][0]['content']['parts'][0]['text'].strip()
                return summary
            except (KeyError, IndexError):
                return "Analysis failed: Unexpected API response format."
        else:
            return f"Analysis failed: API Error {resp.status_code}"
    except Exception as e:
        return f"Analysis failed: {str(e)}"

def main():
    """Main execution point for pipeline integration."""
    print("Brain processing started...")
    
    insights = []
    
    # 1. Process GitHub Data
    github_raw = "skills/self-learning-agent/data/raw/github_events.json"
    if os.path.exists(github_raw):
        import json
        with open(github_raw, "r") as f:
            events = json.load(f)
            for event in events[:3]:
                summary = analyze_text(event.get('content', ''))
                insights.append({
                    "category": f"GitHub ({event.get('type')})",
                    "summary": summary
                })

    # 2. Process X (Twitter) Data
    x_raw = "skills/self-learning-agent/data/raw/x_tweets.json"
    if os.path.exists(x_raw):
        import json
        with open(x_raw, "r") as f:
            tweets = json.load(f)
            for tweet in tweets[:5]:
                author = tweet.get('user', {}).get('screen_name', 'Unknown')
                text = tweet.get('text', '')
                tags = tweet.get('account_tags', [])
                category = tweet.get('account_category', 'X Insight')
                persona = tweet.get('persona', 'Tech Guru')
                
                # Enhanced analysis prompt for X trends
                prompt = f"Analyze this tweet for the '{persona}' persona. Expert: @{author}, Focus: {tags}. Extract one high-value strategic insight: {text}"
                summary = analyze_text_with_prompt(prompt)
                
                insights.append({
                    "category": f"[{persona}] {category}",
                    "summary": f"@{author}: {summary}"
                })
    
    if insights:
        filename = generate_daily_log(insights)
        print(f"Brain: Generated {filename}")
    else:
        print("Brain: No raw data found to process.")

def analyze_text_with_prompt(prompt):
    """Helper for custom prompts."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    try:
        resp = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except:
        pass
    return "Analysis failed."

if __name__ == "__main__":
    # Test run
    sample_text = "The system was rebooted to fix a memory leak in the redis container."
    print(analyze_text(sample_text))

```

### File: pipeline.py
```python

import sys
import os
from dotenv import load_dotenv

# Add src directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import doctor
    import ingest
    import ingest_x
    import brain
    import brain_graph
    import publish
    import release_github
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def main():
    print("--- 🚀 David Agent Pipeline (Flat Mode) ---")
    
    # 1. Doctor
    print("\n[Stage 1] Doctor Check")
    try:
        if not doctor.generate_report():
            print("❌ Health Check Failed. Aborting.")
            return
    except Exception as e:
        print(f"Doctor failed: {e}")
        return

    # 2. Ingest
    print("\n[Stage 2] Ingestion")
    try:
        ingest.fetch_github_events()
        ingest.fetch_self_code()
        # ingest_x.fetch_x_tweets() # Temporarily disabled due to auth/timeout issues
    except Exception as e:
        print(f"Ingestion failed: {e}")

    # 3. Brain
    print("\n[Stage 3] Brain Processing")
    try:
        brain.main()
        brain_graph.process_latest_x_data()
    except Exception as e:
        print(f"Brain failed: {e}")

    # 4. Publish
    print("\n[Stage 4] Publication")
    try:
        publish.main()
        release_github.push_to_github()
    except Exception as e:
        print(f"Publish failed: {e}")

    print("\n--- ✅ Pipeline Completed ---")

if __name__ == "__main__":
    main()

```

### File: doctor.py
```python
import os
import sys
import time
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (force reload)
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path, override=True)

def check_network(host="8.8.8.8", port=53, timeout=3):
    """Check basic network connectivity."""
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.close()
        return True, "Online"
    except Exception as ex:
        return False, f"Offline ({ex})"

def check_gemini():
    """Verify Gemini API connectivity and model availability."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Fallback
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        return False, "Missing GEMINI_API_KEY"
    
    genai.configure(api_key=api_key)
    try:
        # Use config model or default to gemini-3-pro-preview
        model_name = os.getenv("MODEL_DEFAULT", "gemini-3-pro-preview")
        print(f"Testing model: {model_name}")
        model = genai.GenerativeModel(model_name)
        start = time.time()
        # Simple generation
        response = model.generate_content("Ping")
        latency = (time.time() - start) * 1000
        return True, f"Operational ({latency:.0f}ms)"
    except Exception as e:
        # If rate limited, try fallback model
        if "429" in str(e):
            print(f"  ⚠️ Rate limit on {model_name}. Trying fallback gemini-1.5-flash...")
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content("Ping")
                return True, "Operational (Fallback: gemini-2.0-flash)"
            except Exception as e2:
                 return False, f"Error (both models): {e2}"
        return False, f"Error: {e}"

def check_github():
    """Verify GitHub Token and Rate Limits."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return False, "Missing GITHUB_TOKEN"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    try:
        # Check Rate Limit
        resp = requests.get("https://api.github.com/rate_limit", headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # The structure might vary, but usually resources->core
            if 'resources' in data and 'core' in data['resources']:
                core = data['resources']['core']
                remaining = core['remaining']
                limit = core['limit']
                reset_time = time.strftime('%H:%M:%S', time.localtime(core['reset']))
                return True, f"Valid (Quota: {remaining}/{limit}, Resets: {reset_time})"
            else:
                return True, "Valid (Quota info unavailable)"
        elif resp.status_code == 401:
            return False, "Invalid Token (401)"
        else:
            return False, f"API Error ({resp.status_code})"
    except Exception as e:
        return False, f"Connection Error: {e}"

def check_wordpress():
    """Verify WordPress XML-RPC connection."""
    url = os.getenv("WP_URL")
    # user = os.getenv("WP_USERNAME")
    # pwd = os.getenv("WP_PASSWORD")
    
    if not url:
        return False, "Missing WP_URL"
        
    try:
        # Simple POST to check if endpoint is alive
        resp = requests.post(url, headers={'Content-Type': 'text/xml'}, data='<methodCall><methodName>system.listMethods</methodName></methodCall>', timeout=5)
        if resp.status_code == 200:
             return True, "Endpoint Accessible"
        else:
             return False, f"Endpoint Error ({resp.status_code})"
    except Exception as e:
        return False, f"Connection Error: {e}"

def generate_report():
    print("--- 🏥 David Agent Health Check ---")
    
    checks = [
        ("Network (DNS)", check_network("google.com", 80)),
        ("Gemini API", check_gemini()),
        ("GitHub API", check_github()),
        ("WordPress", check_wordpress()),
    ]
    
    all_passed = True
    report = []
    
    print(f"{'COMPONENT':<20} | {'STATUS':<10} | {'DETAILS'}")
    print("-" * 60)
    
    for name, (passed, details) in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            all_passed = False
            status = "❌ FAIL"
        
        # Safe print
        print(f"{name:<20} | {status:<10} | {details}")
        report.append(f"- **{name}**: {status} - {details}")

    # Save report to file
    report_path = "skills/self-learning-agent/data/insights/health_report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write("# David Agent Health Report\n\n")
        f.write(f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("\n".join(report))
        
    return all_passed

if __name__ == "__main__":
    success = generate_report()
    if not success:
        sys.exit(1)

```

### File: publish.py
```python
import os
import glob
import datetime
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client

# Load environment variables
load_dotenv()

WP_URL = os.getenv("WP_URL", "https://dvspace5.wordpress.com/xmlrpc.php")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

INSIGHTS_DIR = "skills/self-learning-agent/data/insights"

def get_latest_log():
    list_of_files = glob.glob(f"{INSIGHTS_DIR}/*.md")
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def publish_to_wordpress(file_path):
    if not file_path:
        print("No learning log found to publish.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Create WordPress client
    try:
        import socket
        socket.setdefaulttimeout(30)
        client = Client(WP_URL, WP_USERNAME, WP_PASSWORD)
    except Exception as e:
        print(f"Failed to connect to WordPress: {e}")
        return

    post = WordPressPost()
    
    # Simple extraction of title from H1
    lines = content.split('\n')
    title = lines[0].replace("# ", "").strip() if lines and lines[0].startswith("# ") else f"Agent Learning Log - {datetime.date.today()}"
    
    post.title = title
    post.content = content
    post.post_status = 'publish'  # or 'draft'
    post.terms_names = {
        'post_tag': ['AI-Agent', 'Self-Learning', 'GitHub'],
        'category': ['Dev Log']
    }

    try:
        post_id = client.call(NewPost(post))
        print(f"Successfully published post {post_id}: {title}")
    except Exception as e:
        print(f"Error publishing to WordPress: {e}")

def main():
    """Main execution point for pipeline integration."""
    latest_log = get_latest_log()
    if latest_log:
        print(f"Publishing log: {latest_log}")
        publish_to_wordpress(latest_log)
    else:
        print("Publish: No logs found.")

if __name__ == "__main__":
    latest_log = get_latest_log()
    if latest_log:
        print(f"Publishing log: {latest_log}")
        publish_to_wordpress(latest_log)
    else:
        print("No logs found.")

```