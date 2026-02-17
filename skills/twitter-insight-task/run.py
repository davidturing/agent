import os
import sys
import json
import time
import random
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

# Try importing XMLRPC
try:
    from wordpress_xmlrpc import Client, WordPressPost
    from wordpress_xmlrpc.methods import posts, media
    from wordpress_xmlrpc.compat import xmlrpc_client
except ImportError:
    print("Error: 'python-wordpress-xmlrpc' is missing. Please run: pip install python-wordpress-xmlrpc")
    exit(1)

# Load environment variables
load_dotenv(override=True)

# Configuration
WP_USER = os.getenv("WORDPRESS_APP_NAME") or "dvspace5"
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

# AI Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_DEFAULT = os.getenv("LLM_MODEL", "gemini-3-pro-preview")

# Target Tweets (Since Search is broken, we manually curate or fetch from a source)
# You can add more URLs here
TARGET_URLS = [
    "https://twitter.com/OpenAI/status/1880000000000000000", # Placeholder, will fail gracefully
    "https://twitter.com/GoogleDeepMind/status/17600000000", # Placeholder
    # Add real URLs below
]

def fetch_tweet_content(tweet_url):
    """
    Fetch tweet content using api.fxtwitter.com (No Auth required).
    """
    print(f"Fetching tweet: {tweet_url}...")
    try:
        parts = tweet_url.split('/')
        if 'status' in parts:
            status_idx = parts.index('status')
            tweet_id = parts[status_idx + 1].split('?')[0]
            username = parts[status_idx - 1]
            
            api_url = f"https://api.fxtwitter.com/{username}/status/{tweet_id}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; DavidAgent/1.0; +https://github.com/)"
            }
            resp = requests.get(api_url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('code') == 200 and 'tweet' in data:
                    tweet = data['tweet']
                    
                    text = tweet.get('text', '')
                    author = tweet.get('author', {}).get('name', 'Unknown')
                    author_id = tweet.get('author', {}).get('screen_name', username)
                    created_at = tweet.get('created_at') # Unix timestamp or string
                    
                    images = []
                    if 'media' in tweet and 'photos' in tweet['media']:
                        for p in tweet['media']['photos']:
                            images.append(p['url'])
                            
                    return {
                        "text": text,
                        "author": author,
                        "username": author_id,
                        "images": images,
                        "url": tweet_url,
                        "created_at": created_at
                    }
            else:
                print(f"  ⚠️ API Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"  ⚠️ Fetch Exception: {e}")
    return None

def summarize_with_gemini(text):
    """Summarize tweet using Gemini REST API with Retry & Fallback."""
    if not text or not GEMINI_API_KEY:
        return None

    models_to_try = [MODEL_DEFAULT, "gemini-2.0-flash"]
    
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        
        prompt = f"""Task: Translate and summarize this tweet into Chinese.
    
Output Format:
TRANSLATION: [Chinese translation]
KEY_POINT: [Core insight in Chinese]

Tweet:
{text}"""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        # Retry loop for 429/Timeout
        for attempt in range(3):
            try:
                print(f"  🤖 AI Summary ({model}, attempt {attempt+1})...")
                response = requests.post(
                    url, 
                    headers={"Content-Type": "application/json"}, 
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "candidates" in data and data["candidates"]:
                        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        return parse_summary_output(raw_text)
                elif response.status_code == 429:
                    print(f"    ⚠️ Rate limit (429). Waiting {5 * (attempt + 1)}s...")
                    time.sleep(5 * (attempt + 1))
                    continue # Retry same model
                else:
                    print(f"    ⚠️ Error {response.status_code}: {response.text}")
                    break # Fatal error for this model, try next model
                    
            except Exception as e:
                print(f"    ⚠️ Exception: {e}")
                time.sleep(2) # Short wait on network error
        
        # If we get here, this model failed after retries. Loop continues to fallback model.
        print(f"  ⚠️ Model {model} failed. Switching to fallback...")

    return None

def parse_summary_output(raw_text):
    html_output = ""
    lines = raw_text.split('\n')
    trans = ""
    point = ""
    
    for line in lines:
        if "TRANSLATION:" in line or "翻译:" in line:
            trans = line.split(":", 1)[1].strip()
        elif "KEY_POINT:" in line or "核心观点:" in line:
            point = line.split(":", 1)[1].strip()
    
    if not trans: trans = raw_text # Fallback
    
    html_output += f"<p><b>翻译:</b> {trans}</p>"
    if point:
        html_output += f"<p><b>核心观点:</b> {point}</p>"
    return html_output

def upload_image_xmlrpc(client, image_url):
    """Upload image via XML-RPC."""
    try:
        resp = requests.get(image_url, timeout=30)
        if resp.status_code != 200: return None
        
        img_data = resp.content
        filename = f"tw_{int(time.time())}_{os.path.basename(image_url.split('?')[0])}"
        if not filename.endswith(('.jpg', '.png', '.jpeg', '.gif')): filename += ".jpg"

        data = {
            'name': filename,
            'type': resp.headers.get('Content-Type', 'image/jpeg'),
            'bits': xmlrpc_client.Binary(img_data),
            'overwrite': False,
        }
        
        response = client.call(media.UploadFile(data))
        return response.get('url')
    except Exception as e:
        print(f"  ⚠️ Image Upload Failed: {e}")
        return None

def run_task(urls):
    print(f"🚀 Starting Task: Processing {len(urls)} URLs via FxTwitter + Gemini...")
    
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"❌ WP Connection Failed: {e}")
        return

    report_html = ""
    has_content = False
    
    for url in urls:
        data = fetch_tweet_content(url)
        if not data:
            continue
            
        print(f"  ✅ Fetched: @{data['username']}")
        
        # Summarize
        summary_html = summarize_with_gemini(data['text'])
        if not summary_html:
            summary_html = f"<p>{data['text']}</p>"
            
        # Images
        img_html = ""
        for img_url in data['images']:
            print(f"    -> Uploading image...")
            wp_url = upload_image_xmlrpc(client, img_url)
            if wp_url:
                img_html += f"<img src='{wp_url}' style='max-width:100%; border-radius:8px; margin-top:10px;' /><br>"
        
        # Build Entry
        report_html += f"<div style='margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px;'>"
        report_html += f"<h3>🐦 <a href='{data['url']}'>@{data['username']}</a></h3>"
        report_html += f"<div style='font-size: 1.1em; margin: 10px 0;'>{summary_html}</div>"
        if img_html:
            report_html += f"<div>{img_html}</div>"
        report_html += f"<p style='color: #888; font-size: 0.9em;'>原文: {data['text'][:100]}...</p>"
        report_html += "</div>"
        
        has_content = True
        time.sleep(1)

    if not has_content:
        print("❌ No content to publish.")
        return

    # Post
    post = WordPressPost()
    post.title = f"Twitter 每日精选 ({datetime.now().strftime('%Y-%m-%d')})"
    post.content = report_html
    post.post_status = 'publish' 
    post.terms_names = {'category': ['AI News', 'Twitter']}
    
    try:
        post_id = client.call(posts.NewPost(post))
        print(f"✅ SUCCESS: Post published! Link: {WP_URL}/?p={post_id}")
    except Exception as e:
        print(f"❌ WP Post Failed: {e}")

if __name__ == "__main__":
    # If args provided, use them
    if len(sys.argv) > 1:
        target_urls = sys.argv[1:]
    else:
        # Default test URL (Musk or OpenAI usually exists)
        target_urls = ["https://twitter.com/OpenAI/status/17600000000"] 
        print("⚠️ No URLs provided. Using placeholder/broken URLs. Pass URLs as arguments to test real data.")
        
    run_task(target_urls)
