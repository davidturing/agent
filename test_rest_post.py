import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing" 
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD") 
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")

def test_rest_api():
    print(f"Connecting to {WP_URL}/wp-json/wp/v2/posts as {WP_USER}...")
    
    # Basic Auth Header
    creds = f"{WP_USER}:{WP_PASSWORD}"
    token = base64.b64encode(creds.encode())
    headers = {
        'Authorization': f'Basic {token.decode("utf-8")}',
        'Content-Type': 'application/json'
    }
    
    post = {
        'title': 'Test Post via REST API',
        'content': 'This is a test post to check REST API connection.',
        'status': 'draft'
    }

    try:
        response = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", json=post, headers=headers)
        if response.status_code == 201:
            print(f"SUCCESS: Created draft post {response.json()['id']}")
        else:
            print(f"FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    test_rest_api()
