import requests
import os
import json
from dotenv import load_dotenv

# Load env
load_dotenv("skills/twitter-insight-task/.env", override=True)

auth_token = os.getenv("X_AUTH_TOKEN")
ct0 = os.getenv("X_CT0")

headers = {
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "x-csrf-token": ct0,
    "cookie": f"auth_token={auth_token}; ct0={ct0}",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-twitter-active-user": "yes",
    "x-twitter-auth-type": "OAuth2Session",
    "x-twitter-client-language": "en"
}

print(f"Testing Auth...")
print(f"Token: {auth_token[:5]}... | CT0: {ct0[:5]}...")

# 1. Verify Credentials (Settings)
url = "https://x.com/i/api/1.1/account/settings.json"
try:
    resp = requests.get(url, headers=headers, timeout=10)
    print(f"\n[Settings Check]")
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("✅ Auth Valid! Username: " + resp.json().get("screen_name", "Unknown"))
    else:
        print(f"❌ Auth Failed: {resp.text[:100]}")
except Exception as e:
    print(f"Error: {e}")

# 2. Try Search (Simple GET v1.1 - Deprecated but sometimes works for simple queries?)
# No, v1.1 search is gone for web. We need GraphQL.
# Let's try to guess a GraphQL query or use a known one.
# This ID is from recent scraping logic, might be outdated.
query_id = "nK1dw4oV3k4w5TdtcAdSww" 
features = {
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": False,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "tweetypie_unmention_optimization_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": False,
    "tweet_awards_web_tipping_enabled": False,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "rweb_video_timestamps_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": True,
    "responsive_web_media_download_video_enabled": False,
    "responsive_web_enhance_cards_enabled": False
}
variables = {
    "rawQuery": "AI min_faves:100",
    "count": 20,
    "querySource": "typed_query",
    "product": "Top"
}

search_url = f"https://x.com/i/api/graphql/{query_id}/SearchTimeline"
# Need to URL encode variables
import urllib.parse
params = {
    "variables": json.dumps(variables),
    "features": json.dumps(features)
}

print(f"\n[Search Check]")
try:
    resp = requests.get(search_url, headers=headers, params=params, timeout=10)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("✅ Search OK!")
        print(f"Response len: {len(resp.text)}")
    else:
        print(f"❌ Search Failed: {resp.text[:200]}")
except Exception as e:
    print(f"Search Error: {e}")
