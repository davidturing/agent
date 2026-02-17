import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

import os
import frontmatter
import re
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, EditPost

# Config
WP_URL = "https://microblocks0.wordpress.com/xmlrpc.php"
WP_USER = "davidturing"
WP_PASS = "d4oy t4ae zq6l kwe4"
ARTICLES_DIR = "microblocks_articles"

def fix_content(content, base_url):
    if not base_url:
        return content

    # Ensure base_url ends with slash
    if not base_url.endswith('/'):
        base_url += '/'
    
    # 1. Fix Markdown images: ![alt](image.png) -> ![alt](base_url/image.png)
    def repl_md_img(match):
        alt = match.group(1)
        src = match.group(2)
        if not src.startswith('http') and not src.startswith('data:'):
            src = base_url + src
        return f"![{alt}]({src})"
    
    content = re.sub(r'!\[(.*?)\]\((.*?)\)', repl_md_img, content)

    # 2. Fix HTML images: <img src="image.png" ...> -> <img src="base_url/image.png" ...>
    def repl_html_img(match):
        tag = match.group(0)
        src_match = re.search(r'src=["\'](.*?)["\']', tag)
        if src_match:
            src = src_match.group(1)
            if not src.startswith('http') and not src.startswith('data:'):
                new_src = base_url + src
                tag = tag.replace(src, new_src)
        return tag
    
    content = re.sub(r'<img[^>]+>', repl_html_img, content)

    # 3. Fix Audio/Video sources: src="file.ogg" -> src="base_url/file.ogg"
    def repl_media_src(match):
        src = match.group(1)
        if not src.startswith('http') and not src.startswith('data:'):
            return f'src="{base_url}{src}"'
        return match.group(0)
        
    content = re.sub(r'src=["\'](.*?\.(?:ogg|mp3|mp4|wav))["\']', repl_media_src, content)

    # 4. Remove specific incompatible divs/classes if needed
    # For now, just fixing links is the priority.
    
    return content

def main():
    print("Connecting to WordPress...")
    client = Client(WP_URL, WP_USER, WP_PASS)
    
    print("Fetching existing posts...")
    # Fetch enough posts to cover the ones we just made
    posts = client.call(GetPosts({'number': 50}))
    post_map = {p.title: p for p in posts}
    
    print(f"Found {len(post_map)} posts.")

    files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
    if not files:
        print("No markdown files found.")
        return

    updated_count = 0
    
    for filename in files:
        filepath = os.path.join(ARTICLES_DIR, filename)
        with open(filepath, 'r') as f:
            post_data = frontmatter.load(f)
        
        title = post_data.get('title')
        original_url = post_data.get('url')
        
        if not original_url:
            print(f"Skipping {filename}: No original URL found in frontmatter.")
            continue

        # Calculate base URL for assets (remove index.html or trailing slash if present, ensure directory path)
        # e.g. .../activities/MIDI-music-en -> .../activities/MIDI-music-en/
        if original_url.endswith('index.html'):
            base_url = original_url.replace('index.html', '')
        elif not original_url.endswith('/'):
            base_url = original_url + '/'
        else:
            base_url = original_url

        if title in post_map:
            print(f"Updating: {title}")
            post = post_map[title]
            
            # Fix the content
            new_content = fix_content(post_data.content, base_url)
            
            # Update fields
            post.content = new_content
            
            # Send update
            client.call(EditPost(post.id, post))
            updated_count += 1
        else:
            print(f"Skipping (not found on WP): {title}")

    print(f"Done. Updated {updated_count} posts.")

if __name__ == "__main__":
    main()
