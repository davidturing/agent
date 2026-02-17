import os
import sys
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")
CT0 = os.getenv("X_CT0")

TARGET_URL = "https://x.com/ohxiyu/status/2020131912149508338"
TARGET_USERNAME = "ohxiyu"
TARGET_ID = "2020131912149508338"

def exec_bird_cmd(cmd_list):
    env = os.environ.copy()
    if AUTH_TOKEN: env["AUTH_TOKEN"] = AUTH_TOKEN
    if CT0: env["CT0"] = CT0
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, env=env)
        return result.stdout.strip()
    except Exception as e:
        print(f"Exec Error: {e}")
        return None

print("=== METHOD 1: Search URL ===")
out1 = exec_bird_cmd(["bird", "search", f"url:{TARGET_URL}", "--json"])
with open("debug_search.json", "w") as f:
    f.write(out1)
print(f"Search output length: {len(out1)}")

print("\n=== METHOD 2: User Timeline ===")
out2 = exec_bird_cmd(["bird", "user-tweets", TARGET_USERNAME, "--json"])
with open("debug_timeline.json", "w") as f:
    f.write(out2)
print(f"Timeline output length: {len(out2)}")

# Quick Analysis
def analyze_json(filename):
    try:
        with open(filename) as f:
            data = json.load(f)
        
        found = False
        for t in data:
            if str(t.get("id")) == TARGET_ID or str(t.get("rest_id")) == TARGET_ID:
                found = True
                print(f"\n[FOUND in {filename}]")
                # Check media
                if "extended_entities" in t:
                    print("  Has extended_entities")
                    media = t["extended_entities"].get("media", [])
                    print(f"  Media count: {len(media)}")
                    for m in media:
                        print(f"    - {m.get('media_url_https')}")
                elif "entities" in t and "media" in t["entities"]:
                    print("  Has entities.media")
                else:
                    print("  NO standard media fields found.")
                    # Dump keys to see what's available
                    print(f"  Keys: {list(t.keys())}")
                    if "legacy" in t:
                        print("  Has 'legacy' field. Checking inside...")
                        leg = t["legacy"]
                        if "extended_entities" in leg:
                            print("    Found extended_entities inside legacy!")
                            media = leg["extended_entities"].get("media", [])
                            print(f"    Media count: {len(media)}")
        if not found:
            print(f"\n[NOT FOUND in {filename}]")
            
    except Exception as e:
        print(f"Error analyzing {filename}: {e}")

analyze_json("debug_search.json")
analyze_json("debug_timeline.json")
