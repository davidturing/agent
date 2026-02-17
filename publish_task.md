# Publishing Task

## Goal
Crawl MicroBlocks activities and publish them to `https://microblocks0.wordpress.com`.

## Credentials
- **User**: `davidturing`
- **Password**: `d4oy t4ae zq6l kwe4` (Application Password)
- **Site**: `microblocks0.wordpress.com`

## Steps

### 1. Connection Check
Before processing all files, verify you can create a post.
Try these endpoints with Basic Auth:
1. `https://public-api.wordpress.com/wp/v2/sites/microblocks0.wordpress.com/posts`
2. `https://public-api.wordpress.com/rest/v1.1/sites/microblocks0.wordpress.com/posts/new`
3. `https://microblocks0.wordpress.com/wp-json/wp/v2/posts`

Create a **draft** post with title "Connection Test".
If it fails, stop and report the error.

### 2. Processing
Read `activities.json` (JSON list of activities).
Filter for `locale === 'en'` (or just use the slugs provided in the previous prompt).

For each activity:
1.  **Check if exists**: (Optional, but good practice) Check if a post with this title already exists to avoid duplicates.
2.  **Fetch Content**: Crawl the `url`.
3.  **Format**:
    -   Convert HTML to Markdown (or clean HTML).
    -   Keep images (use original URLs).
    -   If there's a video, include the link.
4.  **Publish**:
    -   Title: Activity Title
    -   Content: The body text/html.
    -   Status: `publish` (or `draft` if you want to be safe, let's go with `publish`).
    -   Categories: "MicroBlocks Activities" (create if needed, or skip).

### 3. Report
Output a list of published URLs.

## Tools
- Use `curl` or `node` scripts for requests.
- `web_fetch` for crawling content.
