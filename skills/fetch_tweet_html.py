import requests
import re
import json
import os
import sys
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")
CT0 = os.getenv("X_CT0")

def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Cookie": f"auth_token={AUTH_TOKEN}; ct0={CT0}",
        "x-csrf-token": CT0
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.text
    except Exception as e:
        print(f"Request Error: {e}")
        return None

def extract_json_from_html(html):
    # Twitter often puts initial state in a script tag
    # But for logged-in users, it's complex React hydration data.
    # However, sometimes metadata is easier to find.
    
    # Check for meta tags (og:image)
    soup = BeautifulSoup(html, 'html.parser')
    
    images = []
    # OG Images are often just one (the first one)
    og_img = soup.find("meta", property="og:image")
    if og_img:
        images.append(og_img["content"])
        
    # Twitter cards might expose more?
    
    # Try to find JSON blob
    # Often inside <script type="application/json" data-testid="UserProfileSchema-test"> or similar
    
    return images

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_tweet_html.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"Fetching {url}...")
    html = fetch_html(url)
    
    if html:
        # print(html[:500]) # Debug
        images = extract_json_from_html(html)
        print(f"Found {len(images)} images (OG Meta):")
        for img in images:
            print(img)
            
        # Also try regex for typical media url patterns
        # https://pbs.twimg.com/media/.......jpg
        media_pattern = re.compile(r'https://pbs\.twimg\.com/media/[\w-]+\.(?:jpg|png|jpeg)')
        matches = media_pattern.findall(html)
        unique_matches = list(set(matches))
        print(f"Found {len(unique_matches)} media URLs via Regex:")
        for m in unique_matches:
            print(m)
