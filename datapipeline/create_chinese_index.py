import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

import time
from wordpress_xmlrpc import Client, WordPressPage
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost

# Config
WP_URL = "https://microblocks0.wordpress.com/xmlrpc.php"
WP_USER = "davidturing"
WP_PASS = "d4oy t4ae zq6l kwe4"

def categorize_post(title):
    t = title.lower()
    if any(x in t for x in ['getting started', 'first steps', 'intro', 'welcome']):
        return '🚀 入门指南 (Getting Started)'
    if any(x in t for x in ['music', 'sound', 'piano', 'note', 'wav', 'audio', 'theremin']):
        return '🎵 音乐与音频 (Music & Audio)'
    if any(x in t for x in ['robot', 'motor', 'servo', 'car', 'maqueen', 'buggy']):
        return '🤖 机器人与运动 (Robotics & Motion)'
    if any(x in t for x in ['led', 'neopixel', 'display', 'matrix', 'light', 'graphic']):
        return '💡 灯光与显示 (Light & Display)'
    if any(x in t for x in ['sensor', 'temp', 'button', 'input', 'read', 'battery']):
        return '🌡️ 传感器与输入 (Sensors & Inputs)'
    if any(x in t for x in ['radio', 'wifi', 'web', 'http', 'net', 'communication', 'gateway']):
        return '📡 物联网与通信 (Connectivity & IoT)'
    return '🧪 综合项目与实验 (Projects & Experiments)'

def main():
    print("Connecting to WordPress...")
    client = Client(WP_URL, WP_USER, WP_PASS)
    
    print("Fetching published posts...")
    posts = client.call(GetPosts({'number': 100, 'post_status': 'publish', 'post_type': 'post'}))
    
    categories = {
        '🚀 入门指南 (Getting Started)': [],
        '🌡️ 传感器与输入 (Sensors & Inputs)': [],
        '💡 灯光与显示 (Light & Display)': [],
        '🎵 音乐与音频 (Music & Audio)': [],
        '🤖 机器人与运动 (Robotics & Motion)': [],
        '📡 物联网与通信 (Connectivity & IoT)': [],
        '🧪 综合项目与实验 (Projects & Experiments)': []
    }
    
    for p in posts:
        cat = categorize_post(p.title)
        categories[cat].append(p)

    # Generate HTML Content in Chinese
    html = """
    <!-- wp:cover {"overlayColor":"vivid-purple","minHeight":300,"align":"full"} -->
    <div class="wp-block-cover alignfull" style="min-height:300px"><span aria-hidden="true" class="wp-block-cover__background has-vivid-purple-background-color has-background-dim-100 has-background-dim"></span><div class="wp-block-cover__inner-container"><!-- wp:heading {"textAlign":"center","level":1} -->
    <h1 class="has-text-align-center">MicroBlocks 活动指南</h1>
    <!-- /wp:heading -->
    <!-- wp:paragraph {"align":"center","fontSize":"medium"} -->
    <p class="has-text-align-center has-medium-font-size">探索物理计算的乐趣 · 实时交互编程 · 创意无限</p>
    <!-- /wp:paragraph --></div></div>
    <!-- /wp:cover -->

    <!-- wp:heading -->
    <h2>什么是 MicroBlocks?</h2>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph -->
    <p><strong>MicroBlocks</strong> 是一款免费的、类似 Scratch 的图形化编程语言，专门用于微控制器（如 micro:bit, ESP32, Adafruit Circuit Playground 等）。</p>
    <!-- /wp:paragraph -->

    <!-- wp:columns -->
    <div class="wp-block-columns"><!-- wp:column -->
    <div class="wp-block-column"><!-- wp:heading {"level":4} -->
    <h4>⚡ 实时响应 (Live Coding)</h4>
    <!-- /wp:heading -->
    <!-- wp:paragraph -->
    <p>这是 MicroBlocks 最大的特点。你点击积木，硬件就会立刻做出反应，无需漫长的“编译-下载”过程。这让学习和调试变得非常直观。</p>
    <!-- /wp:paragraph --></div>
    <!-- /wp:column -->

    <!-- wp:column -->
    <div class="wp-block-column"><!-- wp:heading {"level":4} -->
    <h4>🔄 并行任务</h4>
    <!-- /wp:heading -->
    <!-- wp:paragraph -->
    <p>MicroBlocks 天生支持多任务。你可以轻松编写程序，让板子在播放音乐的同时闪烁 LED，互不干扰。</p>
    <!-- /wp:paragraph --></div>
    <!-- /wp:column -->

    <!-- wp:column -->
    <div class="wp-block-column"><!-- wp:heading {"level":4} -->
    <h4>💾 独立运行</h4>
    <!-- /wp:heading -->
    <!-- wp:paragraph -->
    <p>代码不仅仅在电脑上运行，它们是真正下载到板子里的。断开 USB 线，接上电池，你的作品就可以独立工作了。</p>
    <!-- /wp:paragraph --></div>
    <!-- /wp:column --></div>
    <!-- /wp:columns -->
    
    <!-- wp:separator -->
    <hr class="wp-block-separator"/>
    <!-- /wp:separator -->

    <!-- wp:heading -->
    <h2>📚 活动清单 (Activity Guide)</h2>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph -->
    <p>以下是为您整理的 MicroBlocks 实验活动，按照主题分类。点击标题即可进入详细教程（中英对照）。</p>
    <!-- /wp:paragraph -->
    """

    for cat_name, post_list in categories.items():
        if not post_list:
            continue
            
        html += f"<!-- wp:heading {{'level':3}} --><h3>{cat_name}</h3><!-- /wp:heading -->"
        html += "<!-- wp:list --><ul>"
        
        # Sort alphabetically within category
        post_list.sort(key=lambda x: x.title)
        
        for p in post_list:
            html += f'<li><a href="{p.link}"><strong>{p.title}</strong></a></li>'
            
        html += "</ul><!-- /wp:list -->"

    # Check if "Activity Guide" page exists to update, else create
    pages = client.call(GetPosts({'post_type': 'page', 'number': 100, 'post_status': 'publish'}))
    target_page = next((p for p in pages if p.title == "Activity Guide"), None)

    if target_page:
        print(f"Updating existing page '{target_page.title}'...")
        target_page.content = html
        client.call(EditPost(target_page.id, target_page))
        print(f"Updated: {target_page.link}")
    else:
        print("Creating new 'Activity Guide' page...")
        page = WordPressPage()
        page.title = "Activity Guide"
        page.content = html
        page.post_status = 'publish'
        page_id = client.call(NewPost(page))
        print(f"Created Page ID {page_id}")

if __name__ == "__main__":
    main()
