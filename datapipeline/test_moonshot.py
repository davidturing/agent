import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MOONSHOT_API_KEY")
print(f"Testing API Key: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.ai/v1",
)

try:
    # Try a simple models list first to check auth
    print("Listing models...")
    models = client.models.list()
    print("Models list success. First model:", models.data[0].id)
    
    # Try a chat completion
    print("Sending chat completion...")
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, verify connection."}
        ],
        temperature=0.3,
    )
    print("Chat response:", completion.choices[0].message.content)
    print("Moonshot API verification: SUCCESS")

except Exception as e:
    print(f"Moonshot API verification: FAILED. Error: {e}")
