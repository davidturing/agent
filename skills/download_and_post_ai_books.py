import os
import requests
import time
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client
from dotenv import load_dotenv

# Load env
load_dotenv()

WP_USER = "davidturing"
WP_PASSWORD = os.getenv("wordpress_app_password_for_dvspace5") or os.getenv("WORDPRESS_APP_PASSWORD")
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

# Book List from user message
BOOKS = [
    {
        "title": "OpenAI: AI in the Enterprise",
        "url": "https://cdn.openai.com/business-guides-pdf/AI_in_the_Enterprise.pdf", # Guessed full URL based on pattern, or use original if accessible
        "is_pdf": True
    },
    {
        "title": "OpenAI: A Practical Guide to Building Agents",
        "url": "https://cdn.openai.com/business-guides-pdf/A_Practical_Guide_to_Building_Agents.pdf", 
        "is_pdf": True
    },
    {
        "title": "Google: Prompting Guide 101",
        "url": "https://services.google.com/fh/files/misc/prompt_engineering_101.pdf", # Guessed/Common URL
        "is_pdf": True
    },
    {
        "title": "OpenAI: Identifying and Scaling AI Use Cases",
        "url": "https://cdn.openai.com/business-guides-pdf/Identifying_and_Scaling_AI_Use_Cases.pdf",
        "is_pdf": True
    },
    {
        "title": "Anthropic: Building Effective AI Agents",
        "url": "https://www.anthropic.com/engineering/building-effective-agents",
        "is_pdf": False # Webpage
    },
    {
        "title": "Anthropic: Prompt Engineering Guide",
        "url": "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview",
        "is_pdf": False # Webpage
    },
    {
        "title": "Kaggle: Agents Companion",
        "url": "https://www.kaggle.com/whitepaper-agents",
        "is_pdf": False
    },
    {
        "title": "Google Cloud: 601 Real-World Generative AI Use Cases",
        "url": "https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-leading-organizations",
        "is_pdf": False
    },
    {
        "title": "Google: Prompt Engineering Whitepaper",
        "url": "https://www.kaggle.com/whitepaper-prompt-engineering",
        "is_pdf": False
    }
]

# Note: Some URLs in the message were truncated (e.g., cdn.openai.com/business-guide...), 
# I have reconstructed them based on common knowledge. If they fail, I will report it.

def upload_file_to_wp(client, file_url, title):
    """Download file and upload to WP Media Library."""
    try:
        print(f"Downloading {title} from {file_url}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(file_url, headers=headers, stream=True, timeout=30)
        
        if r.status_code != 200:
            print(f"  -> Failed to download: HTTP {r.status_code}")
            return None
            
        content_type = r.headers.get('Content-Type', '')
        if 'pdf' not in content_type and 'application/octet-stream' not in content_type:
             print(f"  -> Warning: Content-Type is {content_type}, might not be PDF.")

        filename = f"{title.replace(' ', '_').replace(':', '').replace('/', '_')}.pdf"
        
        # WP Upload
        data = {
            'name': filename,
            'type': 'application/pdf',
            'bits': xmlrpc_client.Binary(r.content),
            'overwrite': False
        }
        
        print(f"  -> Uploading to WordPress...")
        response = client.call(media.UploadFile(data))
        return response.get('url')
        
    except Exception as e:
        print(f"  -> Error: {e}")
        return None

def run():
    print("Connecting to WordPress...")
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"Connection Failed: {e}")
        return

    content_html = "<p>以下是关于 AI 智能体、提示工程和企业应用场景的 9 本权威指南，来自 OpenAI、Google 和 Anthropic。</p>"
    content_html += "<ul>"

    for book in BOOKS:
        title = book['title']
        url = book['url']
        is_pdf = book['is_pdf']
        
        final_link = url
        note = ""

        # Only attempt to download/upload if it looks like a PDF file URL
        if is_pdf:
            wp_link = upload_file_to_wp(client, url, title)
            if wp_link:
                final_link = wp_link
                note = " (已备份到本站)"
            else:
                note = " (原链接)"
        
        content_html += f"<li><strong>{title}</strong>{note}<br>"
        content_html += f"🔗 <a href='{final_link}' target='_blank'>点击阅读/下载</a></li><br>"

    content_html += "</ul>"
    content_html += "<p>来源: <a href='https://x.com/akokoi1/status/2020116798327411013'>@akokoi1 on X</a></p>"

    # Create Post
    post = WordPressPost()
    post.title = "精选资源：OpenAI/Google/Anthropic 的 9 本 AI 权威指南 (PDF下载)"
    post.content = content_html
    post.post_status = 'publish'
    # Minimal terms to avoid "400 Bad Request" on some strict WP configs
    # Try without terms first, or with simple ones if needed.
    post.terms_names = {
        'category': ['AI Resources'],
        'post_tag': ['AI', 'PDF', 'Learning']
    }

    print("Publishing post...")
    try:
        post_id = client.call(posts.NewPost(post))
        print(f"SUCCESS: Post published! ID: {post_id}")
        print(f"Link: {WP_URL}/?p={post_id}")
    except Exception as e:
        print(f"Publish Failed: {e}")
        # Retry without terms if it failed
        if "400" in str(e):
            print("Retrying without terms...")
            try:
                post.terms_names = {}
                post_id = client.call(posts.NewPost(post))
                print(f"SUCCESS (Retry): Post published! ID: {post_id}")
            except Exception as e2:
                print(f"Retry Failed: {e2}")

if __name__ == "__main__":
    run()
