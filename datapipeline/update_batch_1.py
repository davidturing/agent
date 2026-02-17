import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, EditPost

# Config
WP_URL = "https://microblocks0.wordpress.com/xmlrpc.php"
WP_USER = "davidturing"
WP_PASS = "d4oy t4ae zq6l kwe4"

# Content Mapping for "Getting Started" Category
# Generated based on standard MicroBlocks curriculum knowledge
CONTENT_MAP = {
    "Getting Started with micro:bit": {
        "intro": """
        <div class="wp-block-group" style="background-color:#f0f7ff;padding:20px;border-left:5px solid #0073aa;margin-bottom:30px">
        <h3 style="margin-top:0">🚀 实验原理与知识点</h3>
        <p>本教程将带你迈出使用 MicroBlocks 控制 <strong>micro:bit</strong> 的第一步。</p>
        <ul>
        <li><strong>MicroBlocks 环境</strong>：了解如何连接硬件，识别连接状态（绿色圆圈）。</li>
        <li><strong>点阵屏控制 (LED Display)</strong>：学习如何点亮 micro:bit 上的 5x5 LED 矩阵，绘制图形和滚动文字。</li>
        <li><strong>事件驱动 (Events)</strong>：掌握 <code>when button A pressed</code>（当按键A按下时）积木的使用，这是交互式编程的基础。</li>
        <li><strong>循环与动画</strong>：使用 <code>repeat</code> 和 <code>wait</code> 积木制作简单的动画效果。</li>
        </ul>
        </div>
        """,
        "summary": """
        <div class="wp-block-group" style="background-color:#f0fff4;padding:20px;border-left:5px solid #00a32a;margin-top:30px">
        <h3 style="margin-top:0">📝 知识总结</h3>
        <p>恭喜你完成了第一个 MicroBlocks 项目！回顾一下：</p>
        <ol>
        <li>MicroBlocks 是<strong>实时</strong>的，无需反复上传代码。</li>
        <li>你可以通过<strong>事件积木</strong>（如按键按下）来触发程序运行。</li>
        <li>你可以轻松控制 micro:bit 的<strong>显示屏</strong>来输出信息或展示动画。</li>
        </ol>
        <p><strong>挑战一下</strong>：试着修改滚动的文字，或者制作一个心跳动画！</p>
        </div>
        """
    },
    "First steps": {
        "intro": """
        <div class="wp-block-group" style="background-color:#f0f7ff;padding:20px;border-left:5px solid #0073aa;margin-bottom:30px">
        <h3 style="margin-top:0">🚀 实验原理与知识点</h3>
        <p>这是 MicroBlocks 的基础入门课程（基于 Citilab ED1 或通用板子）。你将学习：</p>
        <ul>
        <li><strong>脚本区域</strong>：如何拖拽积木并组合成脚本。</li>
        <li><strong>即时运行</strong>：点击积木即可运行，理解 MicroBlocks 的"活性"。</li>
        <li><strong>控制流</strong>：初步接触循环 (Loops) 和条件判断的概念。</li>
        </ul>
        </div>
        """,
        "summary": """
        <div class="wp-block-group" style="background-color:#f0fff4;padding:20px;border-left:5px solid #00a32a;margin-top:30px">
        <h3 style="margin-top:0">📝 知识总结</h3>
        <p>通过本节课，你已经熟悉了 MicroBlocks 的操作界面。记住，在 MicroBlocks 中，<strong>一切都是并行的</strong>，你可以同时运行多个脚本，这对于后续控制复杂的机器人或传感器任务非常重要。</p>
        </div>
        """
    },
    "Getting Started with Circuit Playground": {
        "intro": """
        <div class="wp-block-group" style="background-color:#f0f7ff;padding:20px;border-left:5px solid #0073aa;margin-bottom:30px">
        <h3 style="margin-top:0">🚀 实验原理与知识点</h3>
        <p>Adafruit Circuit Playground Express (CPX) 是一款功能强大的开发板。本教程将教你：</p>
        <ul>
        <li><strong>NeoPixels</strong>：控制板载的彩色 RGB 灯环，学习设置颜色和亮度。</li>
        <li><strong>传感器读取</strong>：利用板载的各种传感器（光线、声音等）作为输入。</li>
        <li><strong>用户交互</strong>：使用板子上的按钮和开关来控制程序逻辑。</li>
        </ul>
        </div>
        """,
        "summary": """
        <div class="wp-block-group" style="background-color:#f0fff4;padding:20px;border-left:5px solid #00a32a;margin-top:30px">
        <h3 style="margin-top:0">📝 知识总结</h3>
        <p>Circuit Playground 就像一个充满了宝藏的工具箱。通过本实验，你学会了如何点亮它的炫彩灯光并响应用户操作。试着结合光线传感器，做一个"天黑自动亮灯"的小夜灯吧！</p>
        </div>
        """
    },
    "Virtual Dial": {
        "intro": """
        <div class="wp-block-group" style="background-color:#f0f7ff;padding:20px;border-left:5px solid #0073aa;margin-bottom:30px">
        <h3 style="margin-top:0">🚀 实验原理与知识点</h3>
        <p>本实验将介绍<strong>电位器 (Potentiometer)</strong> 的使用，这是一个经典的模拟输入设备。</p>
        <ul>
        <li><strong>模拟信号</strong>：理解数字信号（0/1）与模拟信号（连续变化的值）的区别。</li>
        <li><strong>映射 (Map)</strong>：学习如何将传感器读数（例如 0-1023）映射到我们需要的范围（例如 0-100 或角度 0-180）。</li>
        <li><strong>虚拟交互</strong>：在 MicroBlocks 界面上创建一个虚拟表盘，实时显示硬件旋钮的状态。</li>
        </ul>
        </div>
        """,
        "summary": """
        <div class="wp-block-group" style="background-color:#f0fff4;padding:20px;border-left:5px solid #00a32a;margin-top:30px">
        <h3 style="margin-top:0">📝 知识总结</h3>
        <p>电位器是人机交互的重要元件。你掌握了读取模拟值并将其可视化的方法。这种"硬件控制软件界面"的模式，是很多互动艺术装置的基础。</p>
        </div>
        """
    }
}

def main():
    print("Connecting to WordPress...")
    client = Client(WP_URL, WP_USER, WP_PASS)
    
    print("Fetching posts to update...")
    posts = client.call(GetPosts({'number': 100, 'post_status': 'publish'}))
    
    updated_count = 0
    
    for p in posts:
        if p.title in CONTENT_MAP:
            print(f"Updating: {p.title}...")
            
            data = CONTENT_MAP[p.title]
            original_content = p.content
            
            # Check if already updated (avoid duplication)
            if "实验原理与知识点" in original_content:
                print("  -> Already updated, skipping.")
                continue
                
            # Combine: Intro + Original + Summary
            new_content = data['intro'] + "\n\n" + original_content + "\n\n" + data['summary']
            
            p.content = new_content
            client.call(EditPost(p.id, p))
            print("  -> Done.")
            updated_count += 1
            time.sleep(1)

    print(f"Batch update complete. Updated {updated_count} articles.")

if __name__ == "__main__":
    main()
