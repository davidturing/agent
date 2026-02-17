import collections
try:
    collections.Iterable = collections.abc.Iterable
except AttributeError:
    pass

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.compat import xmlrpc_client
import os
import json
from dotenv import load_dotenv

load_dotenv()

WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing"
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD") or "2oen cgw4 gh5k z3tn"
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)

print("=== Checking Recent Posts (All Status) ===")
try:
    # Fetch recent 10 posts of any status
    recent_posts = client.call(posts.GetPosts({'number': 10, 'post_type': 'post'}))
    for p in recent_posts:
        print(f"ID: {p.id} | Status: {p.post_status} | Title: {p.title}")
except Exception as e:
    print(f"Error fetching posts: {e}")

print("\n=== Checking Ghost IDs (95, 97, 99) ===")
for pid in [95, 97, 99]:
    try:
        p = client.call(posts.GetPost(pid))
        print(f"ID {pid} FOUND:")
        print(f"  Type: {p.post_type}")
        print(f"  Status: {p.post_status}")
        print(f"  Title: {p.title}")
        print(f"  Link: {p.link}")
    except Exception as e:
        print(f"ID {pid} Check Failed: {e}")
