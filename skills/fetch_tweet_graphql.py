import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")
CT0 = os.getenv("X_CT0")

if not AUTH_TOKEN or not CT0:
    print("Error: Missing X_AUTH_TOKEN or X_CT0 in .env")
    sys.exit(1)

def fetch_tweet_details(tweet_id):
    """Fetch full tweet details via GraphQL API using cookies."""
    url = "https://x.com/i/api/graphql/sSjOQYn_1t0g2b-35X8mNA/TweetResultByRestId"
    
    headers = {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "content-type": "application/json",
        "x-csrf-token": CT0,
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "cookie": f"auth_token={AUTH_TOKEN}; ct0={CT0}"
    }

    params = {
        "variables": json.dumps({
            "tweetId": tweet_id,
            "withCommunity": False,
            "includePromotedContent": False,
            "withVoice": False
        }),
        "features": json.dumps({
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        })
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"GraphQL Request Failed: {e}")
        return None

def extract_media(data):
    """Extract media URLs from GraphQL response."""
    media_urls = []
    try:
        result = data.get("data", {}).get("tweetResult", {}).get("result", {})
        legacy = result.get("legacy", {})
        
        # Check standard media
        if "extended_entities" in legacy:
            for m in legacy["extended_entities"].get("media", []):
                if m.get("type") == "photo":
                    media_urls.append(m.get("media_url_https"))
                elif m.get("type") == "video":
                     # For video, extract thumbnail or variant url?
                     # Usually we want the video file, but for blog post image is fine as cover
                     media_urls.append(m.get("media_url_https"))

        # Check for Quoted Status media
        quoted = result.get("quoted_status_result", {}).get("result", {})
        if quoted:
            q_legacy = quoted.get("legacy", {})
            if "extended_entities" in q_legacy:
                print("Found media in Quoted Tweet.")
                for m in q_legacy["extended_entities"].get("media", []):
                    if m.get("type") == "photo":
                        media_urls.append(m.get("media_url_https"))
                    elif m.get("type") == "video":
                        media_urls.append(m.get("media_url_https"))

    except Exception as e:
        print(f"Extraction Error: {e}")
        
    return media_urls

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_tweet_graphql.py <tweet_id>")
        sys.exit(1)
        
    tid = sys.argv[1]
    print(f"Fetching {tid}...")
    data = fetch_tweet_details(tid)
    
    if data:
        # print(json.dumps(data, indent=2)) # Debug
        media = extract_media(data)
        print(f"Found {len(media)} media items:")
        for m in media:
            print(m)
    else:
        print("Failed to fetch.")
