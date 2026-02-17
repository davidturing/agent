import os
import sys
import time
import json
import urllib.request
import urllib.error

def generate_content():
    prompt = """
你是一位专业的摄影教育专家。请为博客 'dvcamera6.wordpress.com' 撰写一篇高质量的文章。

**标题**: 佳能 RF 全家桶实战：从扫街到打鸟的参数进阶

**要求**:
1. 语言：简体中文。
2. 结构与内容：
   - **人像篇 (Portrait Section)**: 使用 Canon R5 + RF 50mm f/1.2 L USM。重点讲解大光圈拍摄和人眼检测自动对焦 (Eye-AF)。
   - **街拍篇 (Street Section)**: 使用 Canon R5 + RF 24-70mm f/2.8 L USM。重点讲解镜头全能性和捕捉动态。
   - **生态篇 (Wildlife Section)**: 使用 Canon R5 + RF 70-200mm f/2.8 L IS USM。重点讲解高快门速度和动物检测对焦。
3. 格式：
   - 使用 HTML 标题 (<h2>)。
   - 规格参数使用无序列表 (<ul>)。
   - 在每个章节插入指定的图片。图片格式为: <img src='https://image.pollinations.ai/prompt/URL_ENCODED_PROMPT' alt='description'>
   - 使用以下 URL 编码后的链接：
     - 人像: https://image.pollinations.ai/prompt/photorealistic%20cinematic%20portrait%20of%20an%20Asian%20woman%20in%20a%20cozy%20bookstore%2C%20warm%20ambient%20light%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2050mm%20f/1.2%20L%20USM%2C%20f/1.2%2C%201/125s%2C%20ISO%20400%2C%20creamy%20bokeh%2C%20extremely%20high%20detail%20skin%20and%20eyes
     - 街拍: https://image.pollinations.ai/prompt/photorealistic%20street%20photography%20of%20a%20busy%20Shanghai%20intersection%20at%20blue%20hour%2C%20motion%20blur%20of%20cars%2C%20sharp%20pedestrian%20crossing%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2024-70mm%20f/2.8%20L%20USM%2C%20f/4%2C%201/30s%2C%20ISO%20800%2C%20vibrant%20city%20colors
     - 生态: https://image.pollinations.ai/prompt/photorealistic%20action%20shot%20of%20a%20kingfisher%20bird%20diving%20into%20water%2C%20splashing%20water%20droplets%20in%20air%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2070-200mm%20f/2.8%20L%20IS%20USM%20at%20200mm%2C%20f/2.8%2C%201/3200s%2C%20ISO%201600%2C%20sharp%20focus%20on%20bird%27s%20eye

请直接输出博文的 HTML 内容，不要包含 Markdown 代码块包裹，也不要包含 <html> 或 <body> 标签。
"""
    
    # HARDCODED for this session if env is missing, but better to check if it's in a file
    # Or I can try to find it in other config files. 
    # For now, let's assume the user wants me to use the model I'm running on if GOOGLE_API_KEY is not available to the subprocess.
    # Actually, as an AI, I can just generate the content myself if I cannot call the API.
    # But the requirement says "explicitly use google/gemini-2.0-flash-001".
    
    # Let's try to get it from a potential config file or ask the user.
    # Wait, I'll check if there's any .env file.
    return None

