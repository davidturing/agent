import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

import requests
import time
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client, WordPressPost, WordPressPage
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from wordpress_xmlrpc.methods.options import SetOptions

# Config
WP_URL = "https://microblocks0.wordpress.com/xmlrpc.php"
WP_USER = "davidturing"
WP_PASS = "d4oy t4ae zq6l kwe4"
SOURCE_JSON = "https://learn.microblocks.fun/activities.json"

def fetch_activity_list():
    print("Fetching activity list...")
    resp = requests.get(SOURCE_JSON)
    resp.raise_for_status()
    all_activities = resp.json()
    # Filter for English
    return [a for a in all_activities if a.get('locale') == 'en']

def fetch_and_process_html(url):
    # Construct base URL for absolute links
    base_url = url
    if base_url.endswith('index.html'):
        base_url = base_url.replace('index.html', '')
    if not base_url.endswith('/'):
        base_url += '/'

    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None

    soup = BeautifulSoup(resp.content, 'html.parser')
    
    # Extract article content
    article = soup.find('article', class_='v_activity__contents')
    if not article:
        article = soup.find('article')
    
    if not article:
        return None, None

    # Extract Summary (First paragraph text)
    summary = ""
    first_p = article.find('p')
    if first_p:
        summary = first_p.get_text(strip=True)
    
    # Fix Images
    for img in article.find_all('img'):
        src = img.get('src')
        if src and not src.startswith(('http:', 'https:', 'data:')):
            if src.startswith('/'):
                img['src'] = 'https://learn.microblocks.fun' + src
            else:
                img['src'] = base_url + src
            if img.has_attr('srcset'): del img['srcset']

    # Fix Audio/Video
    for source in article.find_all('source'):
        src = source.get('src')
        if src and not src.startswith(('http:', 'https:', 'data:')):
             if src.startswith('/'):
                source['src'] = 'https://learn.microblocks.fun' + src
             else:
                source['src'] = base_url + src

    # Fix Links
    for a in article.find_all('a'):
        href = a.get('href')
        if href and not href.startswith(('http:', 'https:', 'mailto:', '#')):
             if href.startswith('/'):
                a['href'] = 'https://learn.microblocks.fun' + href
             else:
                a['href'] = base_url + href

    # Clean up formatting specific to the source site if needed
    # (e.g. remove class names that don't exist on WP)
    # For now, raw HTML is usually fine.

    return str(article), summary

def main():
    client = Client(WP_URL, WP_USER, WP_PASS)
    activities = fetch_activity_list()
    
    print(f"Found {len(activities)} English activities.")
    
    # Cache existing posts to avoid duplicates
    print("Fetching existing WP posts...")
    # Fetch all published posts (limit 100 should cover it)
    existing_posts = client.call(GetPosts({'number': 100, 'post_status': 'publish'}))
    post_map = {p.title: p for p in existing_posts}
    
    processed_activities = [] # List of dicts: {title, url, summary, wp_link}

    for act in activities:
        title = act['title']
        slug = act['slug']
        # Construct source URL (assuming standard structure based on previous pattern)
        # activities.json doesn't always have full URL, usually just slug
        # Pattern: https://learn.microblocks.fun/en/activities/{slug}
        source_url = f"https://learn.microblocks.fun/en/activities/{slug}"
        
        print(f"Processing: {title}...")
        
        html_content, summary = fetch_and_process_html(source_url)
        
        if not html_content:
            print(f"  Failed to scrape content for {title}")
            continue

        wp_post_link = ""
        
        if title in post_map:
            # Update
            post = post_map[title]
            post.content = html_content
            # Ensure published
            post.post_status = 'publish'
            client.call(EditPost(post.id, post))
            wp_post_link = post.link
            print(f"  Updated existing post.")
        else:
            # Create
            post = WordPressPost()
            post.title = title
            post.content = html_content
            post.post_status = 'publish'
            post.slug = slug
            post_id = client.call(NewPost(post))
            # We need the link, but NewPost returns ID. 
            # We can guess or re-fetch, but for index page, let's re-fetch details or just link by ID?
            # Better to link nicely. 
            # Let's create a partial dict and fill link later or assume permalink structure?
            # Safest: GetPost
            # But that is slow. Let's assume standard link structure or fetch only if needed.
            # Actually, WordPressPost object returned by GetPosts has .link
            print(f"  Created new post {post_id}.")
            # Quick fetch to get permalink
            # wp_post_link = client.call(GetPost(post_id)).link # Requires import
            # Optimization: Just use ?p=ID for robustness in the index
            wp_post_link = f"{WP_URL.replace('/xmlrpc.php', '')}/?p={post_id}"

        # If updated, we have the link in post.link (from GetPosts). 
        # If we just scraped post.link from existing_posts map, it works.
        if not wp_post_link and title in post_map:
            wp_post_link = post_map[title].link

        processed_activities.append({
            'title': title,
            'summary': summary or "Learn about this MicroBlocks activity.",
            'wp_link': wp_post_link
        })
        
        time.sleep(0.5) # Polite delay

    # --- Create Index Page ---
    print("\nGenering Index Page...")
    
    index_html = "<!-- wp:paragraph --><p>Welcome to the MicroBlocks Learn archive. Below is a list of available activities and experiments.</p><!-- /wp:paragraph -->"
    index_html += '<table class="wp-block-table"><thead><tr><th>Activity</th><th>Description</th></tr></thead><tbody>'
    
    for item in processed_activities:
        index_html += f"<tr><td><a href='{item['wp_link']}'><strong>{item['title']}</strong></a></td><td>{item['summary']}</td></tr>"
    
    index_html += "</tbody></table>"

    # Check if Index Page exists
    # We look for a page titled "Home" or "Activities Index"
    # Actually, user wants "Home" updated.
    
    # Let's look for a page named "Home"
    pages = client.call(GetPosts({'post_type': 'page', 'number': 20}))
    home_page = next((p for p in pages if p.title.lower() in ['home', 'homepage', 'index']), None)
    
    if home_page:
        print(f"Updating existing page '{home_page.title}'...")
        home_page.content = index_html
        client.call(EditPost(home_page.id, home_page))
        home_page_id = home_page.id
    else:
        print("Creating new 'Home' page...")
        page = WordPressPage()
        page.title = "Home"
        page.content = index_html
        page.post_status = 'publish'
        home_page_id = client.call(NewPost(page))

    # --- Set as Front Page ---
    print(f"Attempting to set Page {home_page_id} as static front page...")
    try:
        # 'show_on_front' = 'page'
        # 'page_on_front' = page_id
        client.call(SetOptions({'show_on_front': 'page', 'page_on_front': home_page_id}))
        print("Successfully set as Front Page.")
    except Exception as e:
        print(f"Could not set front page options (permission/API issue): {e}")
        print("You may need to manually set Settings -> Reading -> Homepage to 'Home' in WP Admin.")

    print("All done.")

if __name__ == "__main__":
    main()
