import requests
import base64
import json

user = "davidturing"
app_password = "d4oy t4ae zq6l kwe4"
site_domain = "microblocks0.wordpress.com"

# Encode credentials for Basic Auth
creds = f"{user}:{app_password}"
token = base64.b64encode(creds.encode()).decode()
headers = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# Test Endpoint 1: WP.com REST API V2
endpoints = [
    f"https://public-api.wordpress.com/wp/v2/sites/{site_domain}/posts",
    f"https://public-api.wordpress.com/rest/v1.1/sites/{site_domain}/posts/new",
    f"https://{site_domain}/wp-json/wp/v2/posts"
]

data = {
    "title": "Connection Test",
    "content": "This is a test post from OpenClaw.",
    "status": "draft"
}

for url in endpoints:
    print(f"\nTesting connection to {url}...")
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}") # Truncate for readability
        
        if response.status_code in [200, 201]:
            print(f"SUCCESS: Draft created on {url}")
            break # Stop on first success
        else:
            print("FAILED.")
            
    except Exception as e:
        print(f"ERROR: {e}")
