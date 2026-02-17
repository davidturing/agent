import requests
from bs4 import BeautifulSoup
import sys

def fetch_nitter(username, tweet_id):
    # Try a few reliable nitter instances
    instances = [
        "https://nitter.poast.org",
        "https://nitter.net",
        "https://nitter.privacydev.net"
    ]
    
    for base in instances:
        url = f"{base}/{username}/status/{tweet_id}"
        print(f"Trying {url}...")
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print(f"Failed {base}: {e}")
            
    return None

def extract_images_from_nitter(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    images = []
    # Nitter usually puts images in <div class="attachments"> -> <div class="image"> -> <a> href=...
    attachments = soup.find("div", class_="attachments")
    if attachments:
        links = attachments.find_all("a", class_="still-image")
        for link in links:
            if link.has_attr("href"):
                # Nitter returns relative or absolute URLs
                img_url = link["href"]
                if not img_url.startswith("http"):
                    img_url = "https://nitter.poast.org" + img_url # Hacky base
                images.append(img_url)
                
    return images

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 fetch_tweet_nitter.py <username> <tweet_id>")
        sys.exit(1)
        
    u = sys.argv[1]
    tid = sys.argv[2]
    
    html = fetch_nitter(u, tid)
    if html:
        imgs = extract_images_from_nitter(html)
        print(f"Found {len(imgs)} images:")
        for i in imgs:
            print(i)
    else:
        print("All Nitter instances failed.")
