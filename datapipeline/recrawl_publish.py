import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

import os
import frontmatter
import re
import requests
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, EditPost

# Config
WP_URL = "https://microblocks0.wordpress.com/xmlrpc.php"
WP_USER = "davidturing"
WP_PASS = "d4oy t4ae zq6l kwe4"
ARTICLES_DIR = "microblocks_articles"

def fetch_and_process_html(url):
    print(f"Fetching {url}...")
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(resp.content, 'html.parser')
    
    # Extract article content
    # Look for <article class="v_activity__contents wysiwyg">
    article = soup.find('article', class_='v_activity__contents')
    if not article:
        # Fallback
        article = soup.find('article')
    
    if not article:
        print("Could not find <article> tag.")
        return None

    # Fix base URL for images
    # e.g. url = .../activities/MIDI-music-en
    # assets are relative to that.
    
    # Ensure url ends with / for base construction if needed, 
    # but requests/bs4 usually handles absolute conversion if we ask nicely?
    # No, we must rewrite src manually.
    
    # Logic: if src is relative, prepend url (dir).
    # If url ends in .html, strip it. 
    # The actual resource base is the directory.
    
    base_url = url
    if base_url.endswith('index.html'):
        base_url = base_url.replace('index.html', '')
    if not base_url.endswith('/'):
        base_url += '/'
        
    # Fix Images
    for img in article.find_all('img'):
        src = img.get('src')
        if src and not src.startswith(('http:', 'https:', 'data:')):
            # It's relative.
            # Handle potential '../' if any (though requests handles resolution better, let's keep it simple)
            # If src starts with /, it's relative to root (learn.microblocks.fun)
            if src.startswith('/'):
                img['src'] = 'https://learn.microblocks.fun' + src
            else:
                img['src'] = base_url + src
                
            # Also fix srcset if present? Usually complex. Let's ignore for now or clear it.
            if img.has_attr('srcset'):
                del img['srcset']

    # Fix Audio/Video
    for source in article.find_all('source'):
        src = source.get('src')
        if src and not src.startswith(('http:', 'https:', 'data:')):
             if src.startswith('/'):
                source['src'] = 'https://learn.microblocks.fun' + src
             else:
                source['src'] = base_url + src

    # Fix Links (href) - optional but good
    for a in article.find_all('a'):
        href = a.get('href')
        if href and not href.startswith(('http:', 'https:', 'mailto:', '#')):
             if href.startswith('/'):
                a['href'] = 'https://learn.microblocks.fun' + href
             else:
                a['href'] = base_url + href

    return str(article)

def main():
    print("Connecting to WordPress...")
    client = Client(WP_URL, WP_USER, WP_PASS)
    
    print("Fetching existing posts...")
    posts = client.call(GetPosts({'number': 100}))
    post_map = {p.title: p for p in posts}
    print(f"Found {len(post_map)} posts on WordPress.")

    files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
    updated_count = 0
    
    for filename in files:
        filepath = os.path.join(ARTICLES_DIR, filename)
        with open(filepath, 'r') as f:
            post_data = frontmatter.load(f)
        
        title = post_data.get('title')
        original_url = post_data.get('url')
        
        if not original_url:
            continue

        if title in post_map:
            print(f"Reprocessing: {title}")
            
            # Fetch fresh HTML
            html_content = fetch_and_process_html(original_url)
            
            if html_content:
                post = post_map[title]
                post.content = html_content
                client.call(EditPost(post.id, post))
                print("  -> Updated.")
                updated_count += 1
            else:
                print("  -> Failed to fetch content.")
        else:
            print(f"Skipping (not on WP): {title}")

    print(f"Done. Refreshed {updated_count} posts from live HTML.")

if __name__ == "__main__":
    main()
