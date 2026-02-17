import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, EditPost

# Config
WP_URL = "https://microblocks0.wordpress.com/xmlrpc.php"
WP_USER = "davidturing"
WP_PASS = "d4oy t4ae zq6l kwe4"

def main():
    print("Connecting to WordPress...")
    client = Client(WP_URL, WP_USER, WP_PASS)
    
    # --- Task 1: Rename Activity Guide Page ---
    print("Updating Home Page Title...")
    # Fetch pages to find 'Activity Guide'
    pages = client.call(GetPosts({'post_type': 'page', 'number': 100, 'post_status': 'publish'}))
    target_page = next((p for p in pages if p.title == "Activity Guide"), None)
    
    if target_page:
        print(f"Found page: {target_page.title} (ID: {target_page.id})")
        target_page.title = "MicroBlock知识分享"
        
        # Also update the heading in content if present
        if "活动清单 (Activity Guide)" in target_page.content:
            target_page.content = target_page.content.replace("活动清单 (Activity Guide)", "MicroBlock知识分享")
            
        client.call(EditPost(target_page.id, target_page))
        print("Page title updated to 'MicroBlock知识分享'.")
    else:
        print("Page 'Activity Guide' not found.")

    # --- Task 2: Rename Duplicate Posts ---
    print("\nChecking for duplicate posts to rename...")
    # Targets to check
    targets = [
        "Getting Started with Circuit Playground",
        "Getting Started with micro:bit",
        "First steps"
    ]
    
    all_posts = client.call(GetPosts({'number': 100, 'post_status': 'publish'}))
    
    for target_title in targets:
        # Find all posts matching this title
        matches = [p for p in all_posts if p.title == target_title]
        
        if len(matches) >= 2:
            print(f"Found {len(matches)} copies of '{target_title}'. Renaming...")
            
            # Sort by ID to keep order stable (usually older ID = published first)
            matches.sort(key=lambda x: int(x.id))
            
            # Rename first to (上)
            post1 = matches[0]
            post1.title = f"{target_title}（上）"
            client.call(EditPost(post1.id, post1))
            print(f"  - Renamed ID {post1.id} to {post1.title}")
            
            # Rename second to (下)
            post2 = matches[1]
            post2.title = f"{target_title}（下）"
            client.call(EditPost(post2.id, post2))
            print(f"  - Renamed ID {post2.id} to {post2.title}")
            
            # If there are more, leave them or rename? User only specified 上/下.
        else:
            print(f"'{target_title}': Found {len(matches)} post(s). No renaming needed.")

    print("\nDone.")

if __name__ == "__main__":
    main()
