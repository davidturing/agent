import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

import os
import frontmatter
import re
import markdown

ARTICLES_DIR = "microblocks_articles"

def fix_links_and_convert(content, base_url):
    if not base_url:
        return markdown.markdown(content, extensions=['extra'])

    if not base_url.endswith('/'):
        base_url += '/'
    
    # Debug print
    # print(f"Base URL: {base_url}")

    def repl_md_img(match):
        alt = match.group(1)
        src = match.group(2)
        if not src.startswith('http') and not src.startswith('data:'):
            src = base_url + src
        # print(f"Fixed MD IMG: {src}")
        return f"![{alt}]({src})"
    
    content = re.sub(r'!\[(.*?)\]\((.*?)\)', repl_md_img, content)

    def repl_html_img(match):
        tag = match.group(0)
        src_match = re.search(r'src=["\'](.*?)["\']', tag)
        if src_match:
            src = src_match.group(1)
            if not src.startswith('http') and not src.startswith('data:'):
                new_src = base_url + src
                tag = tag.replace(src, new_src)
                # print(f"Fixed HTML IMG: {new_src}")
        return tag
    
    content = re.sub(r'<img[^>]+>', repl_html_img, content)
    
    html_content = markdown.markdown(content, extensions=['extra'])
    return html_content

# Test with MIDI-music-en
filename = "MIDI-music-en.md"
filepath = os.path.join(ARTICLES_DIR, filename)
with open(filepath, 'r') as f:
    post_data = frontmatter.load(f)

url = post_data.get('url')
if url.endswith('index.html'):
    base_url = url.replace('index.html', '')
else:
    base_url = url

print(f"Original URL: {url}")
print(f"Base URL: {base_url}")

fixed_html = fix_links_and_convert(post_data.content, base_url)
print("\n--- SAMPLE HTML OUTPUT ---")
print(fixed_html[:1000]) # First 1000 chars
print("\n--- CHECKING FOR IMGS ---")
# Find first img tag
match = re.search(r'<img[^>]+src="([^"]+)"', fixed_html)
if match:
    print(f"Found image src: {match.group(1)}")
else:
    print("No image tags found in output.")
