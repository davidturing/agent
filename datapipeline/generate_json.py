import glob
import re
import json

files = glob.glob("microblocks_articles/*.md")
activities = []

for filepath in files:
    if filepath.endswith("README.md"):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
    if match:
        frontmatter = match.group(1)
        
        item = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                item[key.strip()] = val.strip().strip('"')
        
        # Add locale if missing (filename suffix)
        if 'locale' not in item:
            if filepath.endswith("-en.md"):
                item['locale'] = 'en'
            elif filepath.endswith("-cn.md"):
                item['locale'] = 'cn'
                
        activities.append(item)

with open("activities.json", "w") as f:
    json.dump(activities, f, indent=2)
    
print(f"Generated activities.json with {len(activities)} items.")
