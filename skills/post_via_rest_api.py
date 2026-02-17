import os
import requests
import base64
import json
from dotenv import load_dotenv

load_dotenv()

WP_USER = "davidturing" # Or whatever username works
WP_PASSWORD = os.getenv("wordpress_app_password_for_dvspace5") or os.getenv("WORDPRESS_APP_PASSWORD")
# Site ID or Domain for WP.com API
WP_DOMAIN = "dvspace5.wordpress.com" 
API_BASE = f"https://public-api.wordpress.com/wp/v2/sites/{WP_DOMAIN}"

# Auth Header
def get_auth_header():
    credentials = f"{WP_USER}:{WP_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode()
    return {'Authorization': f'Basic {token}'}

def upload_media(file_url, title):
    """Upload media via REST API."""
    try:
        print(f"Downloading {title}...")
        r = requests.get(file_url, stream=True, timeout=30)
        if r.status_code != 200:
            print(f"  -> Download failed: {r.status_code}")
            return None
        
        filename = f"{title.replace(' ', '_')}.pdf"
        media_url = f"{API_BASE}/media"
        
        headers = get_auth_header()
        headers['Content-Disposition'] = f'attachment; filename={filename}'
        headers['Content-Type'] = 'application/pdf'
        
        print(f"  -> Uploading to WP Media Library...")
        resp = requests.post(media_url, headers=headers, data=r.content)
        
        if resp.status_code == 201:
            data = resp.json()
            return data.get('source_url')
        else:
            print(f"  -> Upload failed: {resp.status_code} - {resp.text}")
            return None

    except Exception as e:
        print(f"  -> Error: {e}")
        return None

def create_post(title, content):
    """Create post via REST API."""
    url = f"{API_BASE}/posts"
    headers = get_auth_header()
    
    data = {
        'title': title,
        'content': content,
        'status': 'publish'
    }
    
    print(f"Publishing post: {title}...")
    resp = requests.post(url, headers=headers, json=data)
    
    if resp.status_code == 201:
        post = resp.json()
        print(f"SUCCESS: Post published! Link: {post.get('link')}")
    else:
        print(f"Publish Failed: {resp.status_code} - {resp.text}")

def run():
    # 1. Correct Links (Manually verified or best effort)
    books = [
        # Verified OpenAI link: https://openai.com/index/ai-in-the-enterprise-guide/ (This is a landing page, PDF is likely gated or behind it)
        # Using placeholder for now as direct PDF links are tricky without browser automation.
        {"title": "OpenAI - AI in the Enterprise", "url": "https://openai.com/index/ai-in-the-enterprise-guide/", "is_pdf": False},
        {"title": "OpenAI - A Practical Guide to Building Agents", "url": "https://openai.com/index/practical-guide-to-building-agents/", "is_pdf": False},
        {"title": "Google - Prompting Guide 101", "url": "https://services.google.com/fh/files/misc/prompt_engineering_101.pdf", "is_pdf": True}, 
        {"title": "OpenAI - Identifying and Scaling AI Use Cases", "url": "https://openai.com/index/identifying-and-scaling-ai-use-cases/", "is_pdf": False},
        {"title": "Anthropic - Building Effective AI Agents", "url": "https://www.anthropic.com/engineering/building-effective-agents", "is_pdf": False},
        {"title": "Anthropic - Prompt Engineering Guide", "url": "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview", "is_pdf": False},
        {"title": "Kaggle - Agents Companion", "url": "https://www.kaggle.com/whitepaper-agents", "is_pdf": False},
        {"title": "Google Cloud - 601 Real-World Generative AI Use Cases", "url": "https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-leading-organizations", "is_pdf": False},
        {"title": "Google - Prompt Engineering Whitepaper", "url": "https://www.kaggle.com/whitepaper-prompt-engineering", "is_pdf": False}
    ]

    content_html = "<p>以下是关于 AI 智能体、提示工程和企业应用场景的 9 本权威指南，来自 OpenAI、Google 和 Anthropic。</p>"
    content_html += "<ul>"

    for book in books:
        title = book['title']
        url = book['url']
        is_pdf = book['is_pdf']
        
        final_link = url
        note = ""

        # Only attempt upload if it's a direct PDF link we are confident in
        if is_pdf:
            # Try to upload
            wp_link = upload_media(url, title)
            if wp_link:
                final_link = wp_link
                note = " (已备份到本站 PDF)"
            else:
                note = " (原链接)"
        
        content_html += f"<li><strong>{title}</strong>{note}<br>"
        content_html += f"🔗 <a href='{final_link}' target='_blank'>点击阅读/下载</a></li><br>"

    content_html += "</ul>"
    content_html += "<p>来源: <a href='https://x.com/akokoi1/status/2020116798327411013'>@akokoi1 on X</a></p>"

    create_post("精选资源：OpenAI/Google/Anthropic 的 9 本 AI 权威指南", content_html)

if __name__ == "__main__":
    run()
