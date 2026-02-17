import os
import glob
import re
import markdown
import requests
import time

USER = "davidturing"
PASSWORD = "d4oy t4ae zq6l kwe4"
XMLRPC_URL = "https://microblocks0.wordpress.com/xmlrpc.php"

def parse_frontmatter(content):
    # Regex to capture frontmatter between --- and ---
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL | re.MULTILINE)
    
    if match:
        frontmatter = match.group(1)
        body = match.group(2)
        
        # Extract title
        title_match = re.search(r'title:\s*"(.*?)"', frontmatter)
        if not title_match:
             title_match = re.search(r'title:\s*(.*)', frontmatter)
             
        title = title_match.group(1).strip('"') if title_match else "Untitled"
        
        return title, body.strip()
        
    return "Untitled", content

def post_to_wp(title, html_content):
    # XML escape content lightly (CDATA handles most, but let's be safe against ]]> inside)
    safe_content = html_content.replace("]]>", "]]]]><![CDATA[>")
    
    xml_payload = f"""<?xml version="1.0"?>
    <methodCall>
      <methodName>wp.newPost</methodName>
      <params>
        <param><value><int>1</int></value></param>
        <param><value><string>{USER}</string></value></param>
        <param><value><string>{PASSWORD}</string></value></param>
        <param>
          <value>
            <struct>
              <member><name>post_title</name><value><string>{title}</string></value></member>
              <member><name>post_content</name><value><string><![CDATA[{safe_content}]]></string></value></member>
              <member><name>post_status</name><value><string>publish</string></value></member>
              <member><name>terms_names</name><value><struct><member><name>category</name><value><array><data><value><string>MicroBlocks Activities</string></value></data></array></value></member></struct></value></member>
            </struct>
          </value>
        </param>
      </params>
    </methodCall>"""
    
    headers = {'Content-Type': 'text/xml'}
    try:
        response = requests.post(XMLRPC_URL, data=xml_payload.encode('utf-8'), headers=headers)
        
        if response.status_code == 200:
            # Extract post ID
            match = re.search(r'<string>(\d+)</string>', response.text)
            if match:
                return match.group(1)
                
            # Sometimes it returns int
            match_int = re.search(r'<int>(\d+)</int>', response.text)
            if match_int:
                return match_int.group(1)
                
        print(f"Error posting '{title}': Status {response.status_code}, {response.text[:200]}")
    except Exception as e:
        print(f"Exception posting '{title}': {e}")
        
    return None

def main():
    files = glob.glob("microblocks_articles/*.md")
    files.sort()
    
    published = []
    
    print(f"Found {len(files)} articles.")
    
    for filepath in files:
        if filepath.endswith("README.md"):
            continue
            
        print(f"Processing {filepath}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            title, md_body = parse_frontmatter(content)
            
            # Convert MD to HTML
            html_body = markdown.markdown(md_body)
            
            # Add a credit line
            html_body += "\n<hr><p><em>Originally from MicroBlocks Learn.</em></p>"
            
            post_id = post_to_wp(title, html_body)
            
            if post_id:
                url = f"https://microblocks0.wordpress.com/?p={post_id}"
                print(f"PUBLISHED: {title} -> {url}")
                published.append(f"- [{title}]({url})")
            else:
                print(f"FAILED: {title}")
                
            time.sleep(2) # Be nice to the API
        except Exception as e:
            print(f"Failed to process {filepath}: {e}")
        
    print("\n--- Summary ---")
    print("\n".join(published))
    
    # Write report
    with open("published_report.md", "w") as f:
        f.write("# Published Articles\n\n")
        f.write("\n".join(published))

if __name__ == "__main__":
    main()
