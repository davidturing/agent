import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MOONSHOT_API_KEY")

print(f"DEBUG: API Key raw: {repr(api_key)}")
if api_key:
    print(f"DEBUG: API Key length: {len(api_key)}")
else:
    print("ERROR: MOONSHOT_API_KEY not found in environment.")
    exit(1)

# URLs to test
urls = [
    "https://api.moonshot.cn/v1/models",
    "https://api.moonshot.ai/v1/models"
]

for url in urls:
    print(f"\nTesting URL: {url}")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
