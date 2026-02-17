import os
import sys
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")
CT0 = os.getenv("X_CT0")

def exec_bird_cmd(cmd_list):
    env = os.environ.copy()
    if AUTH_TOKEN: env["AUTH_TOKEN"] = AUTH_TOKEN
    if CT0: env["CT0"] = CT0
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except Exception:
        return None

def get_tweet_text_bird(tweet_url):
    # Parse username/ID
    try:
        clean_url = tweet_url.split('?')[0]
        output = exec_bird_cmd(["bird", "search", f"url:{clean_url}", "--json"])
        if output:
            try:
                start = output.find('[')
                end = output.rfind(']')
                if start != -1 and end != -1:
                    tweets = json.loads(output[start:end+1])
                    if tweets: return tweets[0]
            except: pass
            
        # Fallback to user-tweets
        parts = tweet_url.split('/')
        status_idx = parts.index('status')
        username = parts[status_idx - 1]
        tweet_id = parts[status_idx + 1].split('?')[0]
        
        output = exec_bird_cmd(["bird", "user-tweets", username, "--json"])
        if output:
            start = output.find('[')
            end = output.rfind(']')
            if start != -1 and end != -1:
                tweets = json.loads(output[start:end+1])
                for t in tweets:
                    if str(t.get("id")) == str(tweet_id):
                        return t
    except:
        return None
    return None

def get_images_gallery_dl(tweet_url):
    cookies_content = f"""
# Netscape HTTP Cookie File
.x.com	TRUE	/	TRUE	0	auth_token	{AUTH_TOKEN}
.x.com	TRUE	/	TRUE	0	ct0	{CT0}
.twitter.com	TRUE	/	TRUE	0	auth_token	{AUTH_TOKEN}
.twitter.com	TRUE	/	TRUE	0	ct0	{CT0}
"""
    cookie_file = f"temp_cookies_{os.getpid()}.txt"
    with open(cookie_file, "w") as f:
        f.write(cookies_content)
        
    try:
        cmd = ["venv/bin/gallery-dl", "--cookies", cookie_file, "--get-urls", tweet_url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(cookie_file): os.remove(cookie_file)
        
        if result.returncode != 0: return []
        return [u for u in result.stdout.strip().split('\n') if u.startswith("http")]
    except:
        if os.path.exists(cookie_file): os.remove(cookie_file)
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No URL provided"}))
        sys.exit(1)
        
    url = sys.argv[1]
    
    # 1. Text
    tweet = get_tweet_text_bird(url)
    text = ""
    username = "Unknown"
    
    if tweet:
        text = tweet.get("full_text") or tweet.get("text")
        username = tweet.get("author", {}).get("username") or tweet.get("user", {}).get("screen_name") or "Unknown"
    
    # 2. Images
    images = get_images_gallery_dl(url)
    
    result = {
        "url": url,
        "text": text,
        "username": username,
        "images": images
    }
    
    print(json.dumps(result))
