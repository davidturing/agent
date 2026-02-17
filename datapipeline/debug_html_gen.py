import os
import frontmatter
import re
import markdown

ARTICLES_DIR = "microblocks_articles"
FILENAME = "MIDI-music-en.md"

def fix_links_and_convert(content, base_url):
    if not base_url:
        return markdown.markdown(content, extensions=['extra'])

    if not base_url.endswith('/'):
        base_url += '/'
    
    print(f"DEBUG: Using base_url: {base_url}")

    # 1. Fix Markdown images
    def repl_md_img(match):
        alt = match.group(1)
        src = match.group(2)
        if not src.startswith('http') and not src.startswith('data:'):
            src = base_url + src
        return f"![{alt}]({src})"
    
    content = re.sub(r'!\[(.*?)\]\((.*?)\)', repl_md_img, content)

    # 2. Fix HTML images
    def repl_html_img(match):
        tag = match.group(0)
        src_match = re.search(r'src=["\'](.*?)["\']', tag)
        if src_match:
            src = src_match.group(1)
            if not src.startswith('http') and not src.startswith('data:'):
                new_src = base_url + src
                # Replace only the src value to preserve other attributes
                # A simple replace on the tag string might be risky if src value appears elsewhere,
                # but for this specific structure it's likely fine.
                # Better: reconstruct the match
                tag = tag.replace(f'src="{src}"', f'src="{new_src}"').replace(f"src='{src}'", f"src='{new_src}'")
        return tag
    
    content = re.sub(r'<img[^>]+>', repl_html_img, content)

    # 3. Fix Audio sources
    def repl_media_src(match):
        src = match.group(1)
        if not src.startswith('http') and not src.startswith('data:'):
            return f'src="{base_url}{src}"'
        return match.group(0)
    
    content = re.sub(r'src=["\'](.*?\.(?:ogg|mp3|mp4|wav))["\']', repl_media_src, content)

    # 4. Remove divs
    content = re.sub(r'<div[^>]*>', '', content)
    content = re.sub(r'</div>', '', content)

    # 5. Convert to HTML
    html_content = markdown.markdown(content, extensions=['extra'])
    return html_content

filepath = os.path.join(ARTICLES_DIR, FILENAME)
with open(filepath, 'r') as f:
    post_data = frontmatter.load(f)

url = post_data.get('url')
if url.endswith('index.html'):
    base_url = url.replace('index.html', '')
else:
    base_url = url

final_html = fix_links_and_convert(post_data.content, base_url)

print(f"\n--- EXTRACTED IMAGE SOURCES FROM {FILENAME} ---")
# Find all img srcs in the final HTML
img_srcs = re.findall(r'<img[^>]+src=["\'](.*?)["\']', final_html)
for i, src in enumerate(img_srcs):
    print(f"Image {i+1}: {src}")

if not img_srcs:
    print("No images found in final HTML!")

# Verify a specific known image
expected_img = "play-MIDI-note-block.png"
found = any(expected_img in src for src in img_srcs)
print(f"\nFound '{expected_img}'? {found}")
