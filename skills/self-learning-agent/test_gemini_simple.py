import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def test_gemini():
    print(f"Testing Gemini API with Key: {API_KEY[:5]}...")
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": "Hello, are you alive?"}]
        }]
    }
    
    try:
        response = requests.post(URL, headers=headers, json=data, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.json()['candidates'][0]['content']['parts'][0]['text'])
            return True
        else:
            print("Error Response:", response.text)
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    test_gemini()
