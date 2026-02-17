import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = "skills/self-learning-agent/pageindex/knowledge"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_DEFAULT = os.getenv("MODEL_DEFAULT", "gemini-3-pro-preview")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_DEFAULT}:generateContent?key={GEMINI_API_KEY}"

def analyze_for_graph(text):
    """Use Gemini to extract entities and relations from text."""
    prompt = f"""
    Analyze the following technical content and extract entities and their relationships.
    Format the output as a JSON list of triples: [subject, relation, object].
    Also suggest a category and sub-topic for storage.
    
    Content: {text}
    
    Response format:
    {{
      "entities": ["entity1", "entity2"],
      "triples": [["entity1", "relation", "entity2"]],
      "category": "CategoryName",
      "topic": "SubTopicName",
      "summary": "Short summary"
    }}
    """
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        resp = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=15)
        if resp.status_code == 200:
            content = resp.json()['candidates'][0]['content']['parts'][0]['text']
            # Basic cleanup of markdown code blocks
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
    except Exception as e:
        print(f"Graph analysis failed: {e}")
    return None

def update_page_index(persona, analysis, raw_text):
    """Store knowledge in the PageIndex directory structure."""
    category = analysis.get("category", "General").replace(" ", "_")
    topic = analysis.get("topic", "Misc").replace(" ", "_")
    
    target_dir = os.path.join(BASE_DIR, persona, category, topic)
    os.makedirs(target_dir, exist_ok=True)
    
    # Save index.md
    index_path = os.path.join(target_dir, "index.md")
    mode = "a" if os.path.exists(index_path) else "w"
    
    with open(index_path, mode, encoding="utf-8") as f:
        if mode == "w":
            f.write(f"# {topic} (Category: {category})\n\n")
        
        f.write(f"## New Insight\n")
        f.write(f"- **Summary**: {analysis.get('summary')}\n")
        f.write(f"- **Relationships**:\n")
        for s, r, o in analysis.get("triples", []):
            f.write(f"  - {s} --({r})--> {o}\n")
        f.write("\n")

    print(f"PageIndex: Updated {index_path}")

def process_latest_x_data():
    x_raw = "skills/self-learning-agent/data/raw/x_tweets.json"
    if not os.path.exists(x_raw):
        return
        
    with open(x_raw, "r") as f:
        tweets = json.load(f)
        
    for tweet in tweets[:3]: # Process top 3 for stability
        text = tweet.get('text', '')
        persona = tweet.get('persona', 'Tech_Guru')
        
        print(f"Analyzing tweet for PageIndex...")
        analysis = analyze_for_graph(text)
        if analysis:
            update_page_index(persona, analysis, text)

if __name__ == "__main__":
    process_latest_x_data()
