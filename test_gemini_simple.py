import google.generativeai as genai
import time

api_key = "AIzaSyA8aaz8LhprxWOA-Rve1yrJldfiZbKHyZA"
genai.configure(api_key=api_key)

try:
    print(f"Testing Gemini API with key: {api_key[:10]}...")
    # Using the model you selected: gemini-3-pro-preview
    model = genai.GenerativeModel('gemini-3-pro-preview')
    
    start = time.time()
    response = model.generate_content("Hello, are you operational?")
    latency = (time.time() - start) * 1000
    
    print(f"--- SUCCESS ---")
    print(f"Model: gemini-3-pro-preview")
    print(f"Latency: {latency:.2f}ms")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"--- FAILED ---")
    print(f"Error: {e}")
