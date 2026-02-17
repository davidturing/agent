import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url="https://api.moonshot.cn/v1",
)

try:
    with open("/Users/zhaoqinhuang/.openclaw/openclaw.json", "r") as f:
        config_content = f.read()

    response = client.chat.completions.create(
        model="kimi-k2-0905-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Analyze the provided JSON configuration file for OpenClaw. Check for missing keys, potential issues, or improvements specifically related to model configuration."},
            {"role": "user", "content": f"Here is the OpenClaw configuration file:\n\n{config_content}"}
        ],
        temperature=0.3,
    )
    
    print(response.choices[0].message.content)

except Exception as e:
    print(f"Error: {e}")
