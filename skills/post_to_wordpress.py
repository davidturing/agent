import os
import sys
import json
import requests
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client
from dotenv import load_dotenv

load_dotenv()

WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing"
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD") or "2oen cgw4 gh5k z3tn"
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

def upload_image_xmlrpc(client, image_url):
    try:
        resp = requests.get(image_url, timeout=30)
        resp.raise_for_status()
        filename = f"tw_{int(time.time())}_{os.path.basename(image_url.split('?')[0])}"
        if not filename.endswith(('jpg','png','jpeg','gif')): filename += ".jpg"
        
        data = {
            'name': filename,
            'type': resp.headers.get('Content-Type', 'image/jpeg'),
            'bits': xmlrpc_client.Binary(resp.content),
            'overwrite': False,
        }
        response = client.call(media.UploadFile(data))
        return response.get('url')
    except Exception as e:
        sys.stderr.write(f"Upload Error: {e}\n")
        return None

def run():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        data = json.loads(input_data)
    except Exception as e:
        print(f"Error parsing input: {e}")
        return

    title = data.get("title", "AI Share")
    content_body = data.get("content", "")
    images = data.get("images", [])
    link = data.get("link", "")
    
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"WP Connection Error: {e}")
        return

    # Build HTML
    html = f"<div style='border-bottom:1px solid #ccc; padding:10px 0;'>"
    html += f"<div style='background-color:#f9f9f9; padding:10px; border-radius:5px;'>{content_body}</div>"
    
    for img_url in images:
        wp_img = upload_image_xmlrpc(client, img_url)
        if wp_img:
            html += f"<img src='{wp_img}' style='max-width:100%; margin-top:10px; display:block;' /><br>"
            
    if link:
        html += f"<p>原文链接: <a href='{link}'>{link}</a></p>"
    html += "</div>"

    post = WordPressPost()
    post.title = title
    post.content = html
    post.post_status = 'publish'
    post.terms_names = {'category': ['AI News'], 'post_tag': ['AI', 'Twitter']}
    
    try:
        pid = client.call(posts.NewPost(post))
        print(f"SUCCESS: {WP_URL}/?p={pid}")
    except Exception as e:
        print(f"Publish Error: {e}")

if __name__ == "__main__":
    run()
