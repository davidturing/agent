import os
import json
import urllib.request
import base64
import sys
import xmlrpc.client

# Configuration
url = "https://dvcamera6.wordpress.com/xmlrpc.php"
username = "davidturing"
password = "5hyx wocr tyom lwef"
image_path = "/Users/zhaoqinhuang/.openclaw/media/inbound/f5d41b29-cbb0-4ab2-ac52-a56aa535d87e.jpg"

def upload_image(token_user, token_pass, file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    
    file_name = os.path.basename(file_path)
    file_type = "image/jpeg"
    
    content = {
        'name': file_name,
        'type': file_type,
        'bits': xmlrpc.client.Binary(data),
        'overwrite': True
    }
    
    server = xmlrpc.client.ServerProxy(url)
    try:
        print(f"Uploading {file_name} to {url}...")
        res = server.wp.uploadFile(0, token_user, token_pass, content)
        return res['url']
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

def create_post(token_user, token_pass, image_url):
    server = xmlrpc.client.ServerProxy(url)
    
    title = "深圳美食：陈鹏鹏潮汕菜"
    body = f"""
    今天和朋友去深圳陈鹏鹏吃潮汕菜，味道非常正宗！
    
    <img src="{image_url}" alt="陈鹏鹏潮汕菜" style="max-width:100%; height:auto;" />
    
    卤水拼盘、砂锅粥、卤猪蹄，每一道都是惊喜。推荐！
    """
    
    post = {
        'title': title,
        'description': body,
        'post_status': 'publish',
        'mt_keywords': ['美食', '深圳', '潮汕菜', '陈鹏鹏']
    }
    
    try:
        print("Creating post...")
        post_id = server.metaWeblog.newPost(0, token_user, token_pass, post, True)
        return post_id
    except Exception as e:
        print(f"Error creating post: {e}")
        return None

if __name__ == "__main__":
    img_url = upload_image(username, password, image_path)
    if img_url:
        print(f"Image uploaded: {img_url}")
        pid = create_post(username, password, img_url)
        if pid:
            print(f"Post created successfully! ID: {pid}")
        else:
            print("Failed to create post.")
    else:
        print("Failed to upload image.")
