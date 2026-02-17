---
name: twitter-insight-v1
description: Run the "AI Twitter Insight Task 01" - Search and fetch latest AI-related tweets from the last 24h, summarize, and post to dvspace5 WordPress.
---

# AI Twitter Insight Task 01 (Search + XML-RPC Version)

This skill runs a Python script that:

1.  **Search Tweets:** Uses `bird` CLI to search for trending AI tweets.
    *   **Keywords:** `AI`, `Artificial Intelligence`, `LLM`, `OpenAI`, `Machine Learning`
    *   **Filter:** `min_faves:50` (Likes > 50)
    *   **Lang:** English or Chinese (`lang:en OR lang:zh`)
    *   **Time:** Last 24 hours (automatic via script logic)

2.  **Summarize & Extract:** Uses Gemini (or configured LLM) to analyze content.
    *   **Summary:** Brief overview of what happened (in Chinese).
    *   **Key Point:** Core insight or opinion (in Chinese).
    *   **Link:** Original link extraction.

3.  **Download Images:** Automatically downloads and re-uploads images from tweets to WordPress.

4.  **Publish Report:** Posts the curated report (text + images) to **dvspace5 WordPress** via XML-RPC.
    *   **Title:** "AI 每日热门资讯 (YYYY-MM-DD)"
    *   **Content:** Author, Time, Summary, Key Point, Images, Original Link.

## Usage
```bash
python3 skills/twitter-insight-task/run.py
```

## Configuration (.env)
You MUST provide Twitter cookies because the official API Free Tier cannot read tweets.
1.  Log in to X.com in your browser.
2.  Open DevTools (F12) -> Application -> Cookies.
3.  Copy `auth_token` and `ct0`.
4.  Add to `.env`:

```bash
X_AUTH_TOKEN="your_auth_token_value"
X_CT0="your_ct0_value"

WORDPRESS_URL="https://dvspace5.wordpress.com"
WORDPRESS_APP_NAME="dvspace5"
WORDPRESS_APP_PASSWORD="your_app_password"

# Optional: LLM Provider (default: gemini)
LLM_PROVIDER="gemini"
GEMINI_API_KEY="your_gemini_key"
```
