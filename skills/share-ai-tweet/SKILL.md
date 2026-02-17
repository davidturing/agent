---
name: share-ai-tweet
description: Auto-process a shared Twitter link (from David) -> Summarize via Gemini -> Post to WeChat Draft Box (or WordPress).
---

# Share AI Tweet

This skill processes a single tweet URL, summarizes it using Gemini, and posts it to either the **WeChat Draft Box** or **WordPress**.

## Usage

### Post to WeChat Draft Box (New Logic)
Use this when you want to create a draft in the WeChat Official Account.
Fixes "Page not found" issues by using `fixupx.com` for robust fetching.

```bash
# Ensure you are in the project root
python3 skills/share-ai-tweet/share_tweet_to_wechat.py <tweet_url>
```

### Post to WordPress (Old Logic)
Use this when you want to post directly to the `dvspace5` WordPress blog.

```bash
python3 skills/share_tweet_to_blog.py <tweet_url>
```

## Requirements
- `GEMINI_API_KEY`
- `WECHAT_APPID` / `WECHAT_APPSECRET` (for WeChat)
- `WORDPRESS_USERNAME` / `WORDPRESS_APP_PASSWORD` (for WordPress)
- `X_AUTH_TOKEN` / `X_CT0` (for old WordPress script fetching)
