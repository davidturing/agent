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
