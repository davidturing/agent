import requests
import sys
import json

def fetch_syndication(tweet_id):
    # Syndication API often used by embeds, doesn't require strict auth
    # But it requires a token calculated from ID usually.
    # However, there is an easier endpoint: https://cdn.syndication.twimg.com/tweet-result?id=...
    # Let's try it. It often requires a 'token' param which is simpler to fake or sometimes optional.
    
    url = f"https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}&lang=en"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Syndication Failed: {r.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    tid = "2020131912149508338" # ohxiyu
    if len(sys.argv) > 1:
        tid = sys.argv[1]
        
    print(f"Fetching {tid} via Syndication...")
    data = fetch_syndication(tid)
    
    if data:
        # Check media
        # Syndication format is different
        # usually data['mediaDetails'] or data['photos']
        if "photos" in data:
            print(f"Found {len(data['photos'])} photos.")
            for p in data['photos']:
                print(p.get("url"))
        elif "video" in data:
            print("Found video.")
            # extract poster or variants
        elif "mediaDetails" in data:
             print(f"Found {len(data['mediaDetails'])} mediaDetails.")
             for m in data['mediaDetails']:
                 print(m.get("media_url_https"))
        else:
            print("No media found in Syndication response.")
            print(list(data.keys()))
