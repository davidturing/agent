import os
import requests
import json
import subprocess
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client
from dotenv import load_dotenv

# Load env
load_dotenv()

WP_USER = "davidturing"
WP_PASSWORD = "2oen cgw4 gh5k z3tn"
WP_URL = "https://dvspace5.wordpress.com"
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

# Twitter Config
AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")
CT0 = os.getenv("X_CT0")

TARGET_TWEET_ID = "2020137802302959665"
TARGET_USERNAME = "akshay_pachaar" # Guessed from URL, will verify

def exec_bird_cmd(cmd_list):
    """Helper to run bird command with auth."""
    env = os.environ.copy()
    if AUTH_TOKEN: env["AUTH_TOKEN"] = AUTH_TOKEN
    if CT0: env["CT0"] = CT0
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            print(f"Bird Error: {result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Exec Error: {e}")
        return None

def get_tweet_details(tweet_id):
    """Fetch tweet details via bird (by searching/timeline)."""
    # Since bird doesn't have 'get-tweet' directly, we often use user-tweets or search
    # Let's try to get user tweets and filter
    print(f"Fetching timeline for {TARGET_USERNAME}...")
    output = exec_bird_cmd(["bird", "user-tweets", TARGET_USERNAME, "--json"])
    if not output: return None

    try:
        start = output.find('[')
        end = output.rfind(']')
        if start != -1 and end != -1:
            tweets = json.loads(output[start:end+1])
            for t in tweets:
                if str(t.get("id")) == str(tweet_id):
                    return t
    except Exception as e:
        print(f"Parse Error: {e}")
    return None

def upload_image_xmlrpc(client, image_url):
    """Upload image via XML-RPC."""
    try:
        resp = requests.get(image_url)
        resp.raise_for_status()
        img_data = resp.content
        filename = f"tw_{int(time.time())}.jpg"
        
        data = {
            'name': filename,
            'type': resp.headers.get('Content-Type', 'image/jpeg'),
            'bits': xmlrpc_client.Binary(img_data),
            'overwrite': False,
        }
        response = client.call(media.UploadFile(data))
        return response.get('url')
    except Exception as e:
        print(f"Image Upload Failed: {e}")
        return None

def run():
    print("Connecting to WordPress...")
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"WP Connection Failed: {e}")
        return

    # 1. Get Tweet
    tweet = get_tweet_details(TARGET_TWEET_ID)
    if not tweet:
        print("Tweet not found in recent timeline. Creating generic post with link.")
        # Fallback if tweet not found in recent fetch
        content_html = f"<p>正在尝试抓取推文 {TARGET_TWEET_ID}...</p><p>请直接访问: <a href='https://x.com/{TARGET_USERNAME}/status/{TARGET_TWEET_ID}'>原文链接</a></p>"
        post = WordPressPost()
        post.title = f"推文分享: @{TARGET_USERNAME} (2020137802302959665)"
        post.content = content_html
        post.post_status = 'publish'
        client.call(posts.NewPost(post))
        return

    # 2. Extract Content
    text = tweet.get("full_text") or tweet.get("text")
    media_list = []
    if "extended_entities" in tweet and "media" in tweet["extended_entities"]:
        media_list = tweet["extended_entities"]["media"]
    
    # 3. Format Post
    # Simple summary (first line as title if possible)
    lines = text.split('\n')
    title = lines[0][:50] + "..." if len(lines[0]) > 50 else lines[0]
    if not title: title = f"分享来自 @{TARGET_USERNAME} 的推文"
    
    content_html = f"<div style='background:#f9f9f9; padding:15px; border-radius:5px;'>"
    content_html += f"<p>{text.replace(chr(10), '<br>')}</p>"
    content_html += "</div>"
    
    # 4. Upload Images
    for m in media_list:
        if m.get("type") == "photo":
            img_url = m.get("media_url_https")
            if img_url:
                wp_img = upload_image_xmlrpc(client, img_url)
                if wp_img:
                    content_html += f"<img src='{wp_img}' style='max-width:100%; margin-top:10px;' /><br>"
    
    content_html += f"<p>原文链接: <a href='https://x.com/{TARGET_USERNAME}/status/{TARGET_TWEET_ID}'>https://x.com/{TARGET_USERNAME}/status/{TARGET_TWEET_ID}</a></p>"

    # 5. Publish
    post = WordPressPost()
    post.title = f"译文: {title}" # TODO: Add translation if needed, for now just repost
    post.content = content_html
    post.post_status = 'publish'
    
    try:
        post_id = client.call(posts.NewPost(post))
        print(f"SUCCESS: Post published! Link: {WP_URL}/?p={post_id}")
    except Exception as e:
        print(f"Publish Failed: {e}")

if __name__ == "__main__":
    run()
