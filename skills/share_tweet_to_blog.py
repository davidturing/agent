import os
import sys
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

# WordPress Config
WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing" # Fallback if not set
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD") or "2oen cgw4 gh5k z3tn"
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

# Twitter Config
AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")
CT0 = os.getenv("X_CT0")

# Gemini Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash-exp" # Try latest experimental
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

def summarize_tweet_gemini(text):
    """Summarize tweet using Gemini REST API."""
    if not text or not GEMINI_API_KEY:
        return None

    prompt = f"""Task: Translate and summarize this tweet into Chinese.
    1. Provide a "TITLE_CN" line with a catchy, short Chinese title based on the content (NOT "Tweet from @user").
    2. Provide a "TRANSLATION" line with the full translation.
    3. Provide a "KEY_POINT" line with core insights.
    
Output Format:
TITLE_CN: [Chinese Title]
TRANSLATION: [Chinese Content]
KEY_POINT: [Core Insight]
LINK: [Original Tweet Link if available in text, else 'N/A']

Tweet:
{text}"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(
            GEMINI_API_URL, 
            headers={"Content-Type": "application/json"}, 
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if "candidates" in data and data["candidates"]:
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return parse_summary_output(raw_text, text)
        else:
            return None
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def parse_summary_output(raw_text, original_text_fallback):
    """Helper to parse the structured output from LLM."""
    html_output = ""
    lines = raw_text.split('\n')
    
    title_cn = ""
    trans = ""
    point = ""
    link = ""
    
    # Debug: Print raw text to see what Gemini returned
    print(f"DEBUG: Gemini Raw Output:\n{raw_text}\n---")

    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith("TITLE_CN:") or line.startswith("TITLE:") or "标题：" in line:
            title_cn = line.split(":", 1)[1].strip()
        elif line.startswith("TRANSLATION:") or line.startswith("SUMMARY:") or "摘要：" in line:
            trans = line.split(":", 1)[1].strip()
        elif line.startswith("KEY_POINT:") or "核心观点：" in line:
            point = line.split(":", 1)[1].strip()
        elif line.startswith("LINK:") or "链接：" in line:
            link = line.split(":", 1)[1].strip()
    
    if not trans and not point:
         # Total failure to parse structure
         # Try to use first line as title if it looks like Chinese
         lines = [l for l in raw_text.split('\n') if l.strip()]
         if lines:
             fallback_title = lines[0][:50]
         else:
             fallback_title = f"分享: {original_text_fallback[:20]}..."
             
         return {
             "title": fallback_title,
             "html": f"<p>{raw_text.replace(chr(10), '<br>')}</p>"
         }

    # If title missing, generate one from translation or original
    if not title_cn:
        if trans:
             title_cn = f"AI 资讯: {trans[:30]}..."
        else:
             title_cn = f"分享: {original_text_fallback[:20]}..."

    html_output += f"<p><b>摘要 (中文):</b> {trans}</p>"
    html_output += f"<p><b>核心观点:</b> {point}</p>"
    if link and link != 'N/A':
        html_output += f"<p><b>链接:</b> <a href='{link}'>{link}</a></p>"
    
    return {
        "title": title_cn,
        "html": html_output
    }

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

def get_tweet_details_with_username(username, tweet_id):
    print(f"Fetching timeline for {username}...")
    output = exec_bird_cmd(["bird", "user-tweets", username, "--json"])
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

def get_tweet_details(tweet_url):
    """Fetch tweet details via bird search (url match)."""
    # Clean URL parameters
    clean_url = tweet_url.split('?')[0]
    
    # bird search "url:<tweet_url>" --json
    # This is often more reliable for specific tweet lookup than user-tweets iteration
    print(f"Searching for tweet: {clean_url}...")
    output = exec_bird_cmd(["bird", "search", f"url:{clean_url}", "--json"])
    
    if output:
        try:
            start = output.find('[')
            end = output.rfind(']')
            if start != -1 and end != -1:
                tweets = json.loads(output[start:end+1])
                if tweets:
                    return tweets[0] # Return first match
        except Exception as e:
            print(f"Search Parse Error: {e}")
            
    # Fallback to user-tweets logic if search fails
    # Parse username from URL
    try:
        parts = tweet_url.split('/')
        status_idx = parts.index('status')
        username = parts[status_idx - 1]
        tweet_id = parts[status_idx + 1].split('?')[0]
        return get_tweet_details_with_username(username, tweet_id)
    except:
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

def get_images_via_gallery_dl(tweet_url):
    """Fetch image URLs using gallery-dl."""
    print(f"Fetching images via gallery-dl for {tweet_url}...")
    
    # Create a temporary cookies.txt for gallery-dl
    # Netscape format: domain flag path secure expiration name value
    cookies_content = f"""
# Netscape HTTP Cookie File
.x.com	TRUE	/	TRUE	0	auth_token	{AUTH_TOKEN}
.x.com	TRUE	/	TRUE	0	ct0	{CT0}
.twitter.com	TRUE	/	TRUE	0	auth_token	{AUTH_TOKEN}
.twitter.com	TRUE	/	TRUE	0	ct0	{CT0}
"""
    cookie_file = "temp_cookies.txt"
    with open(cookie_file, "w") as f:
        f.write(cookies_content)
        
    try:
        # Run gallery-dl to get URLs
        # cmd = ["gallery-dl", "--cookies", cookie_file, "--get-urls", tweet_url]
        # We need to run it via venv python -m gallery_dl usually, or directly if in path
        # But we installed it in venv, so venv/bin/gallery-dl
        cmd = ["venv/bin/gallery-dl", "--cookies", cookie_file, "--get-urls", tweet_url]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Cleanup
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
            
        if result.returncode != 0:
            print(f"gallery-dl Error: {result.stderr.strip()}")
            return []
            
        urls = result.stdout.strip().split('\n')
        urls = [u for u in urls if u.startswith("http")]
        print(f"gallery-dl found {len(urls)} images.")
        return urls
        
    except Exception as e:
        print(f"gallery-dl Exec Error: {e}")
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
        return []

def run(tweet_url):
    print("Connecting to WordPress...")
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"WP Connection Failed: {e}")
        return

    # 1. Get Tweet Text (Bird)
    tweet = get_tweet_details(tweet_url)
    
    if not tweet:
        print("Could not fetch tweet details via Bird CLI.")
        return

    username = tweet.get("author", {}).get("username") or tweet.get("user", {}).get("screen_name") or "Unknown"
    text = tweet.get("full_text") or tweet.get("text")
    
    # 2. Get Images (gallery-dl)
    # We ignore bird's media list and use gallery-dl which is more robust
    image_urls = get_images_via_gallery_dl(tweet_url)
    
    # 3. AI Summary
    print("Generating AI Summary...")
    ai_result = summarize_tweet_gemini(text)
    
    if not ai_result:
        # Fallback
        summary_html = f"<p>{text}</p><p><i>(AI Summary Unavailable)</i></p>"
        post_title = f"分享来自 @{username} 的推文"
    else:
        summary_html = ai_result["html"]
        post_title = ai_result["title"]
    
    # 4. Format Post
    content_html = f"<h2>@{username}</h2>"
    content_html += f"<div style='border-bottom:1px solid #ccc; padding:10px 0;'>"
    content_html += f"<div style='background-color:#f9f9f9; padding:10px; border-radius:5px;'>{summary_html}</div>"
    
    # 5. Upload Images
    uploaded_count = 0
    for img_url in image_urls:
        if img_url:
            print(f"Uploading image: {img_url}...")
            # Gallery-dl gives high res URLs, often ending in .jpg:large etc.
            # WordPress might need clean extension.
            # But XML-RPC upload function handles download->upload, so url is fine.
            wp_img = upload_image_xmlrpc(client, img_url)
            if wp_img:
                content_html += f"<img src='{wp_img}' style='max-width:100%; margin-top:10px; display:block;' /><br>"
                uploaded_count += 1
            else:
                print(f"WARNING: Failed to upload image {img_url}")
    
    if len(image_urls) > 0 and uploaded_count == 0:
        print("WARNING: Media items found by gallery-dl but none uploaded successfully.")
        
    content_html += f"<p>原文链接: <a href='{tweet_url}'>{tweet_url}</a></p>"
    content_html += "</div>"

    # 6. Publish
    post = WordPressPost()
    post.title = post_title # Use AI Generated Title
    post.content = content_html
    post.post_status = 'publish'
    post.terms_names = {
        'category': ['AI News'],
        'post_tag': ['AI', 'Twitter', 'Gemini']
    }
    
    try:
        print(f"Publishing to WordPress: {post_title}...")
        post_id = client.call(posts.NewPost(post))
        print(f"SUCCESS: Post published! Link: {WP_URL}/?p={post_id}")
    except Exception as e:
        print(f"Publish Failed: {e}")
        if "400" in str(e):
             print("Retrying without terms...")
             post.terms_names = {}
             try:
                post_id = client.call(posts.NewPost(post))
                print(f"SUCCESS (Retry): Post published! Link: {WP_URL}/?p={post_id}")
             except Exception as e2:
                print(f"Retry Failed: {e2}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 share_tweet_to_blog.py <tweet_url>")
    else:
        run(sys.argv[1])
