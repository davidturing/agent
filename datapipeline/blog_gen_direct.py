import os
import sys

content = """
<h2>人像篇：RF 50mm f/1.2 L USM 的空气切割感</h2>
<p>在人像摄影中，佳能 EOS R5 搭配 RF 50mm f/1.2 L USM 是当之无愧的“镜皇”组合。其 f/1.2 的超大光圈不仅提供了极浅的景深和奶油般的虚化效果，更在弱光环境下表现卓越。</p>
<img src='https://image.pollinations.ai/prompt/photorealistic%20cinematic%20portrait%20of%20an%20Asian%20woman%20in%20a%20cozy%20bookstore%2C%20warm%20ambient%20light%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2050mm%20f/1.2%20L%20USM%2C%20f/1.2%2C%201/125s%2C%20ISO%20400%2C%20creamy%20bokeh%2C%20extremely%20high%20detail%20skin%20and%20eyes' alt='portrait photography'>
<ul>
    <li><strong>核心技术：</strong> 开启 R5 的“人眼检测自动对焦 (Eye-AF)”，即便在 f/1.2 全开光圈下，系统也能精准锁定模特眼部，确保每一张照片都目光如炬。</li>
    <li><strong>实战参数：</strong> 建议快门不低于 1/125s 以防止微小晃动，ISO 保持在 400 左右以获取最佳纯净度。</li>
</ul>

<h2>街拍篇：RF 24-70mm f/2.8 L USM 的都市韵律</h2>
<p>穿梭在上海的弄堂与摩天大楼之间，镜头的灵活性至关重要。RF 24-70mm f/2.8 L USM 覆盖了从广角到中焦的黄金焦段，是捕捉都市动态的完美利器。</p>
<img src='https://image.pollinations.ai/prompt/photorealistic%20street%20photography%20of%20a%20busy%20Shanghai%20intersection%20at%20blue%20hour%2C%20motion%20blur%20of%20cars%2C%20sharp%20pedestrian%20crossing%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2024-70mm%20f/2.8%20L%20USM%2C%20f/4%2C%201/30s%2C%20ISO%20800%2C%20vibrant%20city%20colors' alt='street photography'>
<ul>
    <li><strong>拍摄进阶：</strong> 尝试使用慢门（如 1/30s）配合镜头防抖，拍摄川流不息的车灯残影，同时保持建筑物的锐利。</li>
    <li><strong>实战参数：</strong> 蓝调时刻建议 ISO 提升至 800，光圈收缩至 f/4 以获得更大的景深，展现城市空间的层次感。</li>
</ul>

<h2>生态篇：RF 70-200mm f/2.8 L IS USM 的瞬间定格</h2>
<p>在生态摄影中，速度决定一切。RF 70-200mm f/2.8 L IS USM 以其极快的对焦速度和紧凑的体积，成为了捕捉飞鸟瞬间的首选。</p>
<img src='https://image.pollinations.ai/prompt/photorealistic%20action%20shot%20of%20a%20kingfisher%20bird%20diving%20into%20water%2C%20splashing%20water%20droplets%20in%20air%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2070-200mm%20f/2.8%20L%20IS%20USM%20at%20200mm%2C%20f/2.8%2C%201/3200s%2C%20ISO%201600%2C%20sharp%20focus%20on%20bird%27s%20eye' alt='wildlife photography'>
<ul>
    <li><strong>核心对焦：</strong> 将 R5 切换至“动物检测优先”，相机能自动识别飞鸟的头部和眼睛，配合高速连拍，抓住翠鸟入水的黄金瞬间。</li>
    <li><strong>实战参数：</strong> 使用 1/3200s 以上的高快门凝固水花，ISO 1600 保证曝光充足，光圈全开 f/2.8 以获得最高的快门潜能。</li>
</ul>
"""

with open("blog_post.html", "w") as f:
    f.write(content)
print("Successfully generated blog_post.html (Static Mock)")
