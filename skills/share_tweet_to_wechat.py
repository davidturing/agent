#!/usr/bin/env python3
"""
Share Tweet to WeChat Draft Box
Fetches a tweet (via FxTwitter API), summarizes it (via Moonshot/Gemini), and creates a draft.
"""

import os
import sys
import json
import requests
import re
import time
from dotenv import load_dotenv

# Add channel script to path
current_dir = os.path.dirname(os.path.abspath(__file__))
# channel script is in .../skills/channel/scripts
channel_script_dir = os.path.abspath(os.path.join(current_dir, 'channel/scripts'))
sys.path.append(channel_script_dir)

try:
    import channel as wechat_channel
except ImportError:
    # Fallback paths
    sys.path.append(os.path.abspath("skills/channel/scripts"))
    try:
        import channel as wechat_channel
    except ImportError:
        print("Error: Could not import 'channel' module.")
        sys.exit(1)

# Load env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")

def fetch_tweet_content(tweet_url):
    """
    Fetch tweet content using api.fxtwitter.com (JSON).
    """
    print(f"Fetching tweet: {tweet_url}...")
    
    try:
        parts = tweet_url.split('/')
        if 'status' in parts:
            status_idx = parts.index('status')
            tweet_id = parts[status_idx + 1].split('?')[0]
            username = parts[status_idx - 1]
            
            api_url = f"https://api.fxtwitter.com/{username}/status/{tweet_id}"
            print(f"Querying API: {api_url}")
            
            resp = requests.get(api_url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('code') == 200 and 'tweet' in data:
                    tweet = data['tweet']
                    text = tweet.get('text', '')
                    author = tweet.get('author', {}).get('name', 'Unknown')
                    
                    images = []
                    if 'media' in tweet and 'photos' in tweet['media']:
                        for p in tweet['media']['photos']:
                            images.append(p['url'])
                            
                    print(f"✅ Fetched via FxTwitter API: {text[:50]}...")
                    return {
                        "text": text,
                        "author": author,
                        "images": images,
                        "url": tweet_url
                    }
    except Exception as e:
        print(f"⚠️ FxTwitter API fetch failed: {e}")
    return None

def parse_summary_output(raw_text, original_text):
    lines = raw_text.split('\n')
    title = ""
    trans = ""
    point = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith("TITLE_CN:") or line.startswith("标题："):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("TRANSLATION:") or line.startswith("翻译："):
            trans = line.split(":", 1)[1].strip()
        elif line.startswith("KEY_POINT:") or line.startswith("观点："):
            point = line.split(":", 1)[1].strip()
            
    if not title: title = "AI 资讯分享"
    
    # Construct Article Content
    content = ""
    # content += f"**{title}**\n\n" # Title used in metadata
    content += f"**摘要**：\n{trans}\n\n"
    content += f"**核心观点**：\n{point}\n\n"
    content += f"**原文**：\n{original_text}\n\n"
    
    return {
        "title": title,
        "content": content,
        "digest": trans[:100]
    }

def summarize_with_moonshot(text):
    """Summarize using Moonshot AI (Kimi)."""
    print("Trying Moonshot AI (Kimi)...")
    if not MOONSHOT_API_KEY:
        print("  -> No MOONSHOT_API_KEY found.")
        return None
        
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MOONSHOT_API_KEY}"
    }
    
    prompt = f"""Task: Translate and summarize this tweet into Chinese.
    
Output Format:
TITLE_CN: [Catchy Chinese Title]
TRANSLATION: [Chinese Translation]
KEY_POINT: [Core Insight]

Tweet:
{text}"""

    data = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        if resp.status_code == 200:
            result = resp.json()
            content = result['choices'][0]['message']['content']
            return parse_summary_output(content, text)
        else:
            print(f"  -> Moonshot Error: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"  -> Moonshot Exception: {e}")
    return None

def call_gemini(model_name, payload):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        return response
    except Exception as e:
        print(f"Error calling {model_name}: {e}")
        return None

def summarize_tweet(text):
    # 1. Try Moonshot
    res = summarize_with_moonshot(text)
    if res: return res

    # 2. Try Gemini
    print("Trying Gemini...")
    if GEMINI_API_KEY:
        payload = {
            "contents": [{
                "parts": [{"text": f"Translate and summarize this to Chinese:\n{text}"}]
            }]
        }
        models = ["gemini-1.5-flash", "gemini-pro"]
        for model in models:
            print(f"  -> Model: {model}...")
            resp = call_gemini(model, payload)
            if resp and resp.status_code == 200:
                data = resp.json()
                if "candidates" in data and data["candidates"]:
                    raw = data["candidates"][0]["content"]["parts"][0]["text"]
                    return parse_summary_output(raw, text)
    
    # 3. Fallback to original text
    print("⚠️ All AI models failed. Using original text.")
    # Create a dummy summary structure
    lines = text.split('\n')
    title = lines[0][:50] + "..." if lines else "Twitter 分享"
    return {
        "title": title,
        "content": f"**原文内容**：\n{text}\n\n(注：AI摘要生成失败，仅展示原文)",
        "digest": text[:100]
    }

def run(tweet_url):
    # 1. Fetch
    tweet_data = fetch_tweet_content(tweet_url)
    if not tweet_data:
        print("❌ Failed to fetch tweet content.")
        return
    
    # 2. Summarize
    print("🤖 Summarizing...")
    summary = summarize_tweet(tweet_data["text"])
    
    if not summary:
        print("❌ AI Summary failed.")
        return
        
    # 3. Create Draft
    print("📝 Creating WeChat Draft...")
    
    full_content = summary["content"]
    print(f"--- Content Preview ---\n{full_content}\n-----------------------")

    access_token = wechat_channel.get_access_token()
    if not access_token:
        print("❌ Could not get WeChat Access Token.")
        return

    full_content = summary["content"]
    
    # Add Images
    uploaded_cover = None
    if tweet_data["images"]:
        for i, img_url in enumerate(tweet_data["images"]):
            try:
                print(f"Downloading image: {img_url}")
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(img_url, headers=headers, timeout=30)
                if r.status_code == 200:
                    tmp_name = f"tmp_img_{int(time.time())}_{i}.jpg"
                    with open(tmp_name, "wb") as f:
                        f.write(r.content)
                    
                    uploaded_url = wechat_channel.upload_image(access_token, tmp_name)
                    if uploaded_url:
                        full_content += f"\n\n<img src='{uploaded_url}' />"
                        if i == 0: uploaded_cover = tmp_name 
                    
                    # Keep cover for a bit, delete others? 
                    # Logic needs cleanup but OS cleans temp eventually or we ignore
            except Exception as e:
                print(f"Image processing failed: {e}")

    full_content += f"\n\n原文链接：{tweet_url}"

    result = wechat_channel.create_draft(
        access_token=access_token,
        title=summary["title"],
        content=full_content,
        author="AI助手",
        cover_image=uploaded_cover 
    )
    
    if uploaded_cover and os.path.exists(uploaded_cover):
        os.remove(uploaded_cover)
    
    wechat_channel.print_result(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 share_tweet_to_wechat.py <tweet_url>")
    else:
        run(sys.argv[1])
