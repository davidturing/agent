import os
import glob
import datetime
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client

# Load environment variables
load_dotenv()

WP_URL = os.getenv("WP_URL", "https://dvspace5.wordpress.com/xmlrpc.php")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

INSIGHTS_DIR = "skills/self-learning-agent/data/insights"

def get_latest_log():
    list_of_files = glob.glob(f"{INSIGHTS_DIR}/*.md")
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def publish_to_wordpress(file_path):
    if not file_path:
        print("No learning log found to publish.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Create WordPress client
    try:
        import socket
        socket.setdefaulttimeout(30)
        client = Client(WP_URL, WP_USERNAME, WP_PASSWORD)
    except Exception as e:
        print(f"Failed to connect to WordPress: {e}")
        return

    post = WordPressPost()
    
    # Simple extraction of title from H1
    lines = content.split('\n')
    title = lines[0].replace("# ", "").strip() if lines and lines[0].startswith("# ") else f"Agent Learning Log - {datetime.date.today()}"
    
    post.title = title
    post.content = content
    post.post_status = 'publish'  # or 'draft'
    post.terms_names = {
        'post_tag': ['AI-Agent', 'Self-Learning', 'GitHub'],
        'category': ['Dev Log']
    }

    try:
        post_id = client.call(NewPost(post))
        print(f"Successfully published post {post_id}: {title}")
    except Exception as e:
        print(f"Error publishing to WordPress: {e}")

def main():
    """Main execution point for pipeline integration."""
    latest_log = get_latest_log()
    if latest_log:
        print(f"Publishing log: {latest_log}")
        publish_to_wordpress(latest_log)
    else:
        print("Publish: No logs found.")

if __name__ == "__main__":
    latest_log = get_latest_log()
    if latest_log:
        print(f"Publishing log: {latest_log}")
        publish_to_wordpress(latest_log)
    else:
        print("No logs found.")
