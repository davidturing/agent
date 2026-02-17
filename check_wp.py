import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from dotenv import load_dotenv

load_dotenv()

WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing" 
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD") 
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

def check_connection():
    print(f"Connecting to {WP_URL} as {WP_USER}...")
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
        recent_posts = client.call(posts.GetPosts({'number': 1}))
        print("Connection Successful!")
        for p in recent_posts:
            print(f"Latest Post: {p.title} (ID: {p.id})")
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    check_connection()
