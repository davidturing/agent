import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from dotenv import load_dotenv

load_dotenv()

WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing" 
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD") 
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

def test_create_post():
    client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    post = WordPressPost()
    post.title = "Test Post Connection"
    post.content = "This is a test post to check XML-RPC connection."
    post.post_status = 'draft'
    
    try:
        post_id = client.call(posts.NewPost(post))
        print(f"SUCCESS: Created draft post {post_id}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_create_post()
