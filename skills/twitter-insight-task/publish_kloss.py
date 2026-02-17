import os
import requests
import time
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client
from dotenv import load_dotenv

load_dotenv()

# Config
WP_USER = os.getenv("wordpress_app_name_for_dvspace5") or os.getenv("WORDPRESS_APP_NAME")
WP_PASSWORD = os.getenv("wordpress_app_password_for_dvspace5") or os.getenv("WORDPRESS_APP_PASSWORD")
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

# Content
HTML_TEMPLATE = """
<h1>@kloss_xyz 每日洞察：AI 赋能与"永久底层"的警告</h1>
<p><strong>日期：</strong> 2026年2月6日</p>
<p><strong>账号：</strong> <a href="https://x.com/kloss_xyz">@kloss_xyz</a> (Systems architecture king)</p>

<h2>核心洞察</h2>
<ul>
<li><strong>超级个体崛起：</strong> AI（特别是 Claude）能够让个人开发者同时维护数十个项目（32个仓库），彻底改变了软件工程的生产力量级。</li>
<li><strong>时代的残酷真相：</strong> 在这个知识免费、创造只需一个 Prompt 的时代，继续选择当"旁观者"（Spectators）的人，可能会沦为"永久的底层阶级"（Permanent underclass）。</li>
</ul>

<hr />

<h2>推文详情分析</h2>

<h3>1. AI 时代的"疯狂"生产力</h3>
<p><strong>发布时间：</strong> 2026-02-06 10:11 UTC</p>
<p>Kloss 分享了他使用 AI 后的工作状态：一个人在几个月内推动了 32 个副业项目（Side Projects），甚至明天就有 11 个新分支准备代码审查。他将这种"混乱但高效"的生活归功于 Claude。</p>
<p><strong>原文：</strong><br /><em>"when you push 32 repos of side projects you’ve been working on for literal months, have 11 new branches ready for review tomorrow, pat yourself on the back, and say thank you claude for organizing that chaotic ass life of mine"</em></p>
<!-- IMAGE_PLACEHOLDER_1 -->

<h3>2. 旁观者 vs. 建设者</h3>
<p><strong>发布时间：</strong> 2026-02-05 19:30 UTC</p>
<p>这是一条充满哲学意味的警告。Kloss 指出，人类历史上大部分知识现在都是免费的，构建应用、艺术、音乐只需一个 Prompt。在这样一个史上最赋能的时代，很多人依然选择只做"观众"。他严厉地指出，这部分人将成为"永久的底层"。</p>
<p><strong>原文：</strong><br /><em>"Most knowledge in human history is entirely free. You can build apps, art, music, and films with your mind. It only requires a prompt. We’re living in the most empowering era humans have ever seen and most of you are choosing to be spectators. That’s the permanent underclass."</em></p>

<hr />
<p><em>此报告由 OpenClaw 自动生成。</em></p>
"""

IMAGES_TO_PROCESS = {
    "<!-- IMAGE_PLACEHOLDER_1 -->": "https://pbs.twimg.com/amplify_video_thumb/2016164421286973440/img/cs3fQzmdk3TSiTVK.jpg"
}

def upload_image(client, url):
    print(f"Uploading {url}...")
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        img_data = resp.content
        filename = f"kloss_{int(time.time())}.jpg"
        
        data = {
            'name': filename,
            'type': 'image/jpeg',
            'bits': xmlrpc_client.Binary(img_data),
            'overwrite': False,
        }
        res = client.call(media.UploadFile(data))
        return res.get('url')
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

def main():
    print("Connecting to WordPress...")
    try:
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"WP Connection Failed: {e}")
        return

    final_html = HTML_TEMPLATE
    
    # Process Images
    for placeholder, url in IMAGES_TO_PROCESS.items():
        wp_url = upload_image(client, url)
        if wp_url:
            img_tag = f'<img src="{wp_url}" alt="Twitter Media" style="max-width:100%; height:auto; margin:10px 0;" />'
            final_html = final_html.replace(placeholder, img_tag)
        else:
            final_html = final_html.replace(placeholder, "")

    # Create Post
    print("Creating draft post...")
    post = WordPressPost()
    post.title = "@kloss_xyz 洞察：AI 时代的创造力与阶层分化"
    post.content = final_html
    post.post_status = 'draft' # Safety first
    # post.terms_names = {'category': ['AI Insights']} 

    try:
        post_id = client.call(posts.NewPost(post))
        print(f"SUCCESS: Draft created! Post ID: {post_id}")
        print(f"Preview Link: {WP_URL}/?p={post_id}")
    except Exception as e:
        print(f"Failed to create post: {e}")

if __name__ == "__main__":
    main()
