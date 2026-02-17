#!/usr/bin/env python3
"""
Share WeChat Article to WordPress
Fetches content from a WeChat MP URL, summarizes it, checks moderation, and posts to WordPress.
"""

import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client
import time

# Load env
load_dotenv()

# WordPress Config
WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing" 
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD") 
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

# AI Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")

def fetch_wechat_content(url_or_path):
    """Fetch and parse WeChat article content (URL or local file)."""
    print(f"Fetching WeChat article: {url_or_path}...")
    
    try:
        if os.path.exists(url_or_path):
            with open(url_or_path, 'rb') as f:
                content = f.read()
            url = "Local File"
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            }
            resp = requests.get(url_or_path, headers=headers, timeout=60)
            resp.raise_for_status()
            content = resp.content
            url = url_or_path
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Title
        title_tag = soup.find('meta', property='og:title')
        title = title_tag['content'] if title_tag else soup.title.string if soup.title else "WeChat Article"
        
        # Author
        author_tag = soup.find('meta', property='og:article:author')
        author = author_tag['content'] if author_tag else "WeChat"
        
        # Content (WeChat content is usually in #js_content)
        content_div = soup.find(id='js_content')
        if not content_div:
            # Fallback to body text or meta tags
            text = soup.get_text(separator='\n', strip=True)
            if len(text) < 500: # If body text is too short, use meta tags
                 desc = soup.find('meta', property='og:description')
                 desc_content = desc['content'] if desc else ""
                 text = f"{title}\n\n{desc_content}\n\n(Note: Full content could not be fetched due to WeChat protection. This is a summary based on metadata.)"
            html = str(soup.body)
        else:
            # Remove scripts and styles
            for script in content_div(["script", "style"]):
                script.extract()
            text = content_div.get_text(separator='\n', strip=True)
            html = str(content_div)
            
        # Images (extract first few unique images)
        images = []
        if content_div:
            for img in content_div.find_all('img'):
                src = img.get('data-src') or img.get('src')
                if src and src.startswith('http'):
                    images.append(src)
        
        return {
            "title": title,
            "author": author,
            "text": text,
            "html": html,
            "images": images[:5], # Limit images
            "url": url
        }

    except Exception as e:
        print(f"❌ Fetch failed: {e}")
        return None

def moderate_content(text):
    """Check if content violates WordPress.com ToS using LLM."""
    if not text:
        return False, "Empty content"

    prompt = f"""Task: Audit the following content for violation of WordPress.com Terms of Service.
    
    The ToS prohibits:
    - Unlawful purposes or illegal content
    - Infringement of intellectual property
    - Spam or bulk unsolicited messages
    - Malware, spyware, or malicious code
    - Hateful, offensive, or indecent content (though some freedom is allowed, we want to be safe)
    
    Content to audit (truncated):
    {text[:2000]}...
    
    Output Format:
    SAFE: [Yes/No]
    REASON: [Brief explanation if No]
    """

    try:
        # 1. Try Moonshot
        if MOONSHOT_API_KEY:
            url = "https://api.moonshot.cn/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {MOONSHOT_API_KEY}"
            }
            data = {
                "model": "moonshot-v1-8k",
                "messages": [
                    {"role": "system", "content": "You are a content moderator."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            }
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            if resp.status_code == 200:
                result = resp.json()['choices'][0]['message']['content']
                if "SAFE: Yes" in result or "SAFE:Yes" in result:
                    return True, "Safe"
                else:
                    return False, result.split("REASON:")[-1].strip() if "REASON:" in result else result
        
        # 2. Try Gemini
        if GEMINI_API_KEY:
             payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
             url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
             resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
             if resp.status_code == 200:
                 data = resp.json()
                 if "candidates" in data and data["candidates"]:
                    result = data["candidates"][0]["content"]["parts"][0]["text"]
                    if "SAFE: Yes" in result or "SAFE:Yes" in result:
                        return True, "Safe"
                    else:
                        return False, result.split("REASON:")[-1].strip() if "REASON:" in result else result

        # Fallback
        return False, "No LLM available for moderation"

    except Exception as e:
        print(f"  - Moderation Error: {e}")
        return False, f"Moderation check failed: {e}"

def parse_summary_output(raw_text):
    lines = raw_text.split('\n')
    title = ""
    summary = ""
    point = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith("TITLE_CN:") or line.startswith("标题："):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("SUMMARY:") or line.startswith("摘要："):
            summary = line.split(":", 1)[1].strip()
        elif line.startswith("KEY_POINT:") or line.startswith("观点："):
            point = line.split(":", 1)[1].strip()
            
    if not title: title = "WeChat Article Share"
    
    # HTML Content for WordPress (Summary part)
    summary_html = f"<div style='background-color:#f9f9f9; padding:15px; border-radius:8px; border-left: 4px solid #0073aa; margin-bottom: 20px;'>"
    if summary: summary_html += f"<p><strong>摘要</strong>：{summary}</p>"
    if point: summary_html += f"<p><strong>核心观点</strong>：{point}</p>"
    summary_html += "</div>"
    
    return {
        "title": title,
        "summary_html": summary_html
    }

def summarize_content(text):
    """Summarize content."""
    print("🤖 Summarizing...")
    
    prompt = f"""Task: Summarize this article into Chinese.
    
Output Format:
TITLE_CN: [Catchy Chinese Title]
SUMMARY: [Concise summary]
KEY_POINT: [Core Insight]

Content (truncated):
{text[:6000]}"""

    # Try Moonshot
    if MOONSHOT_API_KEY:
        try:
            url = "https://api.moonshot.cn/v1/chat/completions"
            headers = {"Authorization": f"Bearer {MOONSHOT_API_KEY}"}
            data = {
                "model": "moonshot-v1-8k",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            if resp.status_code == 200:
                return parse_summary_output(resp.json()['choices'][0]['message']['content'])
        except Exception as e:
            print(f"Moonshot Error: {e}")

    # Try Gemini
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if "candidates" in data:
                    return parse_summary_output(data["candidates"][0]["content"]["parts"][0]["text"])
        except Exception as e:
            print(f"Gemini Error: {e}")

    return {"title": "Article Share", "summary_html": "<p>Summary unavailable.</p>"}

def upload_image_xmlrpc(client, image_url):
    """Upload image via XML-RPC."""
    # Skip data URIs
    if image_url.startswith('data:'): return None
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://mp.weixin.qq.com/" # WeChat images need referer
        }
        resp = requests.get(image_url, headers=headers, timeout=15)
        resp.raise_for_status()
        img_data = resp.content
        
        filename = f"wx_{int(time.time())}.jpg"
        
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

def run(url_or_path, original_url=None):
    # 1. Fetch
    data = fetch_wechat_content(url_or_path)
    if not data: return
    
    if original_url:
        data['url'] = original_url

    # 2. Moderation
    print("🛡️ Moderating content...")
    is_safe, reason = moderate_content(data["text"])
    if not is_safe:
        print(f"❌ Content BLOCKED by ToS Check: {reason}")
        return

    # 3. Summarize
    summary = summarize_content(data["text"])

    # 4. Connect WP
    print("Connecting to WordPress...")
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"WP Connection Failed: {e}")
        return

    # 5. Upload Images
    uploaded_images = []
    print(f"Found {len(data['images'])} images. Uploading...")
    for img_url in data['images']:
        wp_url = upload_image_xmlrpc(client, img_url)
        if wp_url:
            uploaded_images.append(wp_url)
            print(f"  -> Uploaded: {wp_url}")

    # 6. Build Content
    content_html = f"<h3>来自 {data['author']} 的分享</h3>"
    content_html += summary["summary_html"]
    
    content_html += "<h5>原文图片精选</h5>"
    if uploaded_images:
        for img in uploaded_images:
            content_html += f"<img src='{img}' style='max-width:100%; margin-bottom:10px; display:block; border-radius:4px;' />"
    
    content_html += f"<p>原文链接: <a href='{data['url']}'>{data['url']}</a></p>"

    # 7. Publish
    post = WordPressPost()
    post.title = summary["title"]
    post.content = content_html
    post.post_status = 'publish'
    post.terms_names = {'category': ['AI News'], 'post_tag': ['WeChat', 'Summary']}

    try:
        print(f"Publishing: {summary['title']}...")
        post_id = client.call(posts.NewPost(post))
        print(f"SUCCESS: Post published! Link: {WP_URL}/?p={post_id}")
    except Exception as e:
        print(f"Publish Failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 share_wechat_to_wordpress.py <url_or_path> [original_url]")
    else:
        orig = sys.argv[2] if len(sys.argv) > 2 else None
        run(sys.argv[1], orig)
