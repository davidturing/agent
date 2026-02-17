import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

import time
from wordpress_xmlrpc import Client, WordPressPage
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost

# Config
WP_URL = "https://microblocks0.wordpress.com/xmlrpc.php"
WP_USER = "davidturing"
WP_PASS = "d4oy t4ae zq6l kwe4"

def categorize_post(title):
    t = title.lower()
    if any(x in t for x in ['getting started', 'first steps', 'intro', 'welcome']):
        return 'Getting Started'
    if any(x in t for x in ['music', 'sound', 'piano', 'note', 'wav', 'audio']):
        return 'Music & Audio'
    if any(x in t for x in ['robot', 'motor', 'servo', 'car', 'maqueen', 'buggy']):
        return 'Robotics & Motion'
    if any(x in t for x in ['led', 'neopixel', 'display', 'matrix', 'light', 'graphic']):
        return 'Light & Display'
    if any(x in t for x in ['sensor', 'temp', 'button', 'input', 'read']):
        return 'Sensors & Inputs'
    if any(x in t for x in ['radio', 'wifi', 'web', 'http', 'net', 'communication']):
        return 'Connectivity & IoT'
    return 'Projects & Experiments'

def main():
    print("Connecting to WordPress...")
    client = Client(WP_URL, WP_USER, WP_PASS)
    
    print("Fetching published posts...")
    # Fetch all posts to generate the index
    posts = client.call(GetPosts({'number': 100, 'post_status': 'publish', 'post_type': 'post'}))
    
    # Sort/Group
    categories = {
        'Getting Started': [],
        'Sensors & Inputs': [],
        'Light & Display': [],
        'Music & Audio': [],
        'Robotics & Motion': [],
        'Connectivity & IoT': [],
        'Projects & Experiments': []
    }
    
    for p in posts:
        cat = categorize_post(p.title)
        categories[cat].append(p)

    # Generate HTML Content
    html = """
    <!-- wp:heading -->
    <h2>Introduction</h2>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph -->
    <p>Welcome to the MicroBlocks Activity Hub. This collection features over 60 hands-on projects designed to help you master physical computing with MicroBlocks. From blinking your first LED to building complex IoT gateways, these activities cover a wide range of topics suitable for beginners and advanced users alike.</p>
    <!-- /wp:paragraph -->

    <!-- wp:paragraph -->
    <p>MicroBlocks is a blocks-based programming language that runs right inside your microcontroller, making it incredibly fast and interactive. Below you will find a categorized list of all available tutorials.</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:separator -->
    <hr class="wp-block-separator"/>
    <!-- /wp:separator -->
    """

    for cat_name, post_list in categories.items():
        if not post_list:
            continue
            
        html += f"<!-- wp:heading {{'level':3}} --><h3>{cat_name}</h3><!-- /wp:heading -->"
        html += "<!-- wp:list --><ul>"
        
        # Sort alphabetically within category
        post_list.sort(key=lambda x: x.title)
        
        for p in post_list:
            # Create a simple summary if we don't have one handy (fetching content is slow)
            # We'll just link the title for now as a clean index.
            html += f'<li><a href="{p.link}"><strong>{p.title}</strong></a></li>'
            
        html += "</ul><!-- /wp:list -->"

    # Check if "Activity Guide" page exists to update, else create
    pages = client.call(GetPosts({'post_type': 'page', 'number': 100, 'post_status': 'publish'}))
    target_page = next((p for p in pages if p.title == "Activity Guide"), None)

    if target_page:
        print(f"Updating existing page '{target_page.title}'...")
        target_page.content = html
        client.call(EditPost(target_page.id, target_page))
        print(f"Updated: {target_page.link}")
    else:
        print("Creating new 'Activity Guide' page...")
        page = WordPressPage()
        page.title = "Activity Guide"
        page.content = html
        page.post_status = 'publish'
        page_id = client.call(NewPost(page))
        print(f"Created Page ID {page_id}")

if __name__ == "__main__":
    main()
