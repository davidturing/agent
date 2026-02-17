import os
import datetime
import requests
import tweepy
import time
import base64
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# 1. Load Credentials
load_dotenv()

X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
X_CONSUMER_SECRET = os.getenv("X_CONSUMER_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

WP_USER = "dvspace5" # Hardcoded based on instructions, but could use env
WP_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")
WP_SITE_DOMAIN = "dvspace5.wordpress.com"
WP_API_URL = f"https://public-api.wordpress.com/wp/v2/sites/{WP_SITE_DOMAIN}"

TARGET_ACCOUNTS = [
    "kloss_xyz", "rryssf_", "0xROAS", "AmirMushich", "TerosEso", 
    "DjaniWhaleSkul", "lets_ash", "ai_uncovered", "tomkrcha", "paoloanzn", 
    "yevrrah", "aryanXmahajan", "VibeMarketer_", "hajKuron", "maxxmalist", 
    "theahmedkaiz", "BusDownBonnor", "NotLucknite", "vriparbelli", "rokbercic"
]

def get_twitter_client():
    auth = tweepy.OAuth1UserHandler(
        X_CONSUMER_KEY, X_CONSUMER_SECRET,
        X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth)

def translate_text(text):
    try:
        if not text:
            return ""
        # Split text if too long (Google Translate limit is usually ~5000 chars, tweets are short)
        return GoogleTranslator(source='auto', target='zh-CN').translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def upload_image_to_wp(img_url, title):
    try:
        # Download image
        img_resp = requests.get(img_url)
        if img_resp.status_code != 200:
            return None
        
        filename = f"tweet_img_{int(time.time())}_{title[:5]}.jpg"
        
        # Upload to WordPress
        media_url = f"{WP_API_URL}/media"
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode(),
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "image/jpeg"
        }
        
        response = requests.post(media_url, headers=headers, data=img_resp.content)
        if response.status_code == 201:
            return response.json().get('source_url')
        else:
            print(f"Failed to upload image: {response.text}")
            return None
    except Exception as e:
        print(f"Image upload error: {e}")
        return None

def create_wp_post(content_html):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    title = f"Twitter 每日洞察 ({today})"
    
    post_url = f"{WP_API_URL}/posts"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode(),
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "content": content_html,
        "status": "draft" 
    }
    
    response = requests.post(post_url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json().get('link')
    else:
        print(f"Failed to create post: {response.text}")
        return None

def main():
    print("Starting script...")
    api = get_twitter_client()
    
    # Check credentials
    try:
        user = api.verify_credentials()
        print(f"Authenticated as {user.name}")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    cutoff_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)
    
    all_tweets_html = ""
    
    for screen_name in TARGET_ACCOUNTS:
        print(f"Fetching tweets for @{screen_name}...")
        try:
            # exclude_replies=True to focus on their content, include_rts=False (optional, user didn't specify, but usually better for "insights")
            tweets = api.user_timeline(screen_name=screen_name, count=10, tweet_mode="extended", exclude_replies=True, include_rts=False)
            
            user_tweets_html = ""
            found_tweets = False
            
            for tweet in tweets:
                created_at = tweet.created_at.replace(tzinfo=datetime.timezone.utc)
                if created_at < cutoff_time:
                    continue
                
                found_tweets = True
                print(f"  - Processing tweet from {created_at}")
                
                # Text
                original_text = tweet.full_text
                translated_text = translate_text(original_text)
                
                # Images
                media_urls = []
                if 'media' in tweet.entities:
                    for media in tweet.entities['media']:
                        if media['type'] == 'photo':
                            media_urls.append(media['media_url'])
                
                # Build HTML for this tweet
                tweet_html = f'<div style="border:1px solid #ddd; padding:15px; margin-bottom:20px; border-radius:8px;">'
                tweet_html += f'<h3>@{screen_name} - {created_at.strftime("%H:%M")}</h3>'
                tweet_html += f'<p><strong>原文:</strong> {original_text}</p>'
                tweet_html += f'<p><strong>译文:</strong> {translated_text}</p>'
                
                if media_urls:
                    tweet_html += '<div style="display:flex; gap:10px; flex-wrap:wrap;">'
                    for m_url in media_urls:
                        # Upload to WP
                        wp_img_url = upload_image_to_wp(m_url, screen_name)
                        if wp_img_url:
                             tweet_html += f'<img src="{wp_img_url}" style="max-width:300px; height:auto;">'
                        else:
                             # Fallback to hotlink if upload fails
                             tweet_html += f'<img src="{m_url}" style="max-width:300px; height:auto;">'
                    tweet_html += '</div>'
                    
                tweet_html += f'<p><a href="https://twitter.com/{screen_name}/status/{tweet.id}" target="_blank">View Original</a></p>'
                tweet_html += '</div>'
                
                user_tweets_html += tweet_html
            
            if found_tweets:
                all_tweets_html += f"<h2>Latest from @{screen_name}</h2>{user_tweets_html}<hr>"
                
        except Exception as e:
            print(f"Error fetching {screen_name}: {e}")
            
    if not all_tweets_html:
        print("No tweets found in the last 24 hours.")
        # Create an empty post anyway or just exit?
        # User wants a report, so I'll create a post saying "No updates".
        all_tweets_html = "<p>过去 24 小时内监控账户无新推文。</p>"
    
    print("Creating WordPress post...")
    post_link = create_wp_post(all_tweets_html)
    
    if post_link:
        print(f"SUCCESS: Post created at {post_link}")
    else:
        print("FAILED to create post.")

if __name__ == "__main__":
    main()
